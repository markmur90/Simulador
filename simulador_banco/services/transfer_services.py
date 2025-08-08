import random
import datetime
import logging
from typing import Any, Dict
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from banco.models import Transfer, DebtorAccount, OTPChallenge, LogTransferencia, PaymentIdentification, AccountMovement, Debtor, Creditor, CreditorAccount, CreditorAgent, PostalAddress
import uuid

logger = logging.getLogger(__name__)

class TransferService:
    RATE_LIMIT = 5
    WINDOW_MINUTES = 5

    @staticmethod
    @transaction.atomic
    def ingest_transfer(data: Dict[str, Any]) -> Transfer:
        """
        Recibe los datos de transferencia enviados por la API y los procesa.
        Los datos esperados son los mismos que envía send_transfer:
        - payment_id: str
        - debtor_account: str (nombre/IBAN)
        - creditor_account: str (nombre/IBAN)
        - debtor: str (nombre)
        - creditor: str (nombre)
        - creditor_agent: str (BIC)
        - instructed_amount: float
        - currency: str
        - requested_execution_date: str
        - purpose_code: str
        - remittance_information_unstructured: str
        - payment_identification: str o None
        - auth_id: str
        - status: str
        """
        logger.debug("Iniciando ingest_transfer")
        logger.debug(f"Datos recibidos de la API: {data}")
        
        try:
            # Extraer payment_id del payload de la API
            payment_id = data.get("payment_id")
            if not payment_id:
                payment_id = str(uuid.uuid4())
                data["payment_id"] = payment_id
            logger.debug(f"Payment ID recibido: {payment_id}")

            # Verificar si ya existe una transferencia con este payment_id
            existing = Transfer.objects.filter(payment_id=payment_id).first()
            if existing:
                logger.debug(f"Transferencia existente encontrada con payment_id: {payment_id}")
                return existing

            # Procesar datos que vienen de la API (strings) y convertirlos a objetos
            processed_data = TransferService._process_api_data(data)
            
            window_start = timezone.now() - datetime.timedelta(minutes=TransferService.WINDOW_MINUTES)
            recent_count = Transfer.objects.filter(
                debtor_account=processed_data["debtor_account"],
                created_at__gte=window_start
            ).count()
            logger.debug(f"Transferencias recientes para la cuenta: {recent_count}")
            
            if recent_count >= TransferService.RATE_LIMIT:
                logger.debug(f"Límite de transferencias excedido para la cuenta")
                processed_data["status"] = 'RJCT'
                return Transfer.objects.create(**processed_data)

            # Crear PaymentIdentification con UUIDs válidos si no existe
            logger.debug("Creando PaymentIdentification")
            if not processed_data.get("payment_identification"):
                payment_identification = PaymentIdentification.objects.create(
                    end_to_end_id=uuid.uuid4(),
                    instruction_id=uuid.uuid4()
                )
                processed_data["payment_identification"] = payment_identification
            else:
                logger.debug(f"PaymentIdentification existente: {processed_data['payment_identification']}")
            
            processed_data["status"] = 'PDNG'
            logger.debug(f"PaymentIdentification procesado: {processed_data['payment_identification']}")

            # Crear la transferencia
            logger.debug("Creando transferencia")
            transfer = Transfer.objects.create(**processed_data)
            logger.debug(f"Transferencia creada con ID: {transfer.id}")

            # Generar OTP
            logger.debug("Generando OTP")
            otp = f"{random.randint(100000, 999999)}"
            otp_challenge = OTPChallenge.objects.create(
                payment_id=payment_id,
                otp=otp,
                status="CREATED"
            )
            logger.debug(f"OTP generado: {otp_challenge.otp}")

            # Registrar en el log
            logger.debug("Registrando log de la transferencia")
            LogTransferencia.objects.create(
                registro=payment_id,
                tipo_log='CREATED',
                contenido=f'Transferencia creada: {transfer.instructed_amount} {transfer.currency}'
            )

            return transfer

        except Exception as e:
            import traceback
            logger.error("Error en ingest_transfer:")
            logger.error(f"Tipo de error: {type(e).__name__}")
            logger.error(f"Mensaje de error: {str(e)}")
            logger.error("Traceback completo:")
            logger.error(traceback.format_exc())
            
            # Registrar el error en el log
            LogTransferencia.objects.create(
                registro=str(uuid.uuid4()),
                tipo_log='ERROR',
                contenido=f'Error en ingest_transfer: {str(e)}\n{traceback.format_exc()}'
            )
            
            raise ValidationError(f"Error al procesar la transferencia: {str(e)}")

    @staticmethod
    def _process_api_data(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa los datos que vienen de la API y los convierte al formato esperado por el modelo.
        La API envía nombres de objetos en lugar de objetos completos.
        """
        processed_data = data.copy()
        
        # Procesar debtor_account (la API envía el nombre, necesitamos el objeto)
        if "debtor_account" in processed_data and isinstance(processed_data["debtor_account"], str):
            try:
                debtor_account = DebtorAccount.objects.get(iban=processed_data["debtor_account"])
                processed_data["debtor_account"] = debtor_account
                logger.debug(f"DebtorAccount encontrado: {debtor_account}")
            except DebtorAccount.DoesNotExist:
                # Si no existe, crear uno por defecto
                logger.warning(f"DebtorAccount no encontrado para IBAN: {processed_data['debtor_account']}")
                
                # Asegurar que tenemos un debtor antes de crear la cuenta
                if "debtor" not in processed_data or not isinstance(processed_data["debtor"], Debtor):
                    # Crear debtor por defecto si no existe
                    postal_address, _ = PostalAddress.objects.get_or_create(
                        country="ES",
                        street="Dirección por defecto",
                        city="Ciudad por defecto"
                    )
                    
                    default_debtor, created = Debtor.objects.get_or_create(
                        name="Deudor por defecto",
                        defaults={
                            "customer_id": str(uuid.uuid4())[:35],
                            "address": postal_address
                        }
                    )
                    processed_data["debtor"] = default_debtor
                    logger.debug(f"Debtor por defecto creado/asignado: {default_debtor}")
                
                debtor_account = DebtorAccount.objects.create(
                    iban=processed_data["debtor_account"],
                    currency=processed_data.get("currency", "EUR"),
                    debtor=processed_data["debtor"]
                )
                processed_data["debtor_account"] = debtor_account
                logger.debug(f"DebtorAccount creado: {debtor_account}")

        # Procesar creditor_account (la API envía el nombre, necesitamos el objeto)
        if "creditor_account" in processed_data and isinstance(processed_data["creditor_account"], str):
            try:
                creditor_account = CreditorAccount.objects.get(iban=processed_data["creditor_account"])
                processed_data["creditor_account"] = creditor_account
                logger.debug(f"CreditorAccount encontrado: {creditor_account}")
            except CreditorAccount.DoesNotExist:
                # Si no existe, crear uno por defecto
                logger.warning(f"CreditorAccount no encontrado para IBAN: {processed_data['creditor_account']}")
                
                # Asegurar que tenemos un creditor antes de crear la cuenta
                if "creditor" not in processed_data or not isinstance(processed_data["creditor"], Creditor):
                    # Crear creditor por defecto si no existe
                    postal_address, _ = PostalAddress.objects.get_or_create(
                        country="ES",
                        street="Dirección por defecto",
                        city="Ciudad por defecto"
                    )
                    
                    default_creditor, created = Creditor.objects.get_or_create(
                        name="Acreedor por defecto",
                        defaults={
                            "address": postal_address
                        }
                    )
                    processed_data["creditor"] = default_creditor
                    logger.debug(f"Creditor por defecto creado/asignado: {default_creditor}")
                
                creditor_account = CreditorAccount.objects.create(
                    iban=processed_data["creditor_account"],
                    currency=processed_data.get("currency", "EUR"),
                    creditor=processed_data["creditor"]
                )
                processed_data["creditor_account"] = creditor_account
                logger.debug(f"CreditorAccount creado: {creditor_account}")

        # Procesar debtor (la API envía el nombre, necesitamos el objeto)
        if "debtor" in processed_data and isinstance(processed_data["debtor"], str):
            try:
                debtor = Debtor.objects.get(name=processed_data["debtor"])
                processed_data["debtor"] = debtor
                logger.debug(f"Debtor encontrado: {debtor}")
            except Debtor.DoesNotExist:
                # Si no existe, crear uno por defecto
                logger.warning(f"Debtor no encontrado para nombre: {processed_data['debtor']}")
                
                # Crear PostalAddress primero
                postal_address = PostalAddress.objects.create(
                    country="ES",
                    street="Dirección por defecto",
                    city="Ciudad por defecto"
                )
                
                debtor = Debtor.objects.create(
                    name=processed_data["debtor"],
                    customer_id=str(uuid.uuid4())[:35],
                    address=postal_address
                )
                processed_data["debtor"] = debtor
                logger.debug(f"Debtor creado: {debtor}")

        # Procesar creditor (la API envía el nombre, necesitamos el objeto)
        if "creditor" in processed_data and isinstance(processed_data["creditor"], str):
            try:
                creditor = Creditor.objects.get(name=processed_data["creditor"])
                processed_data["creditor"] = creditor
                logger.debug(f"Creditor encontrado: {creditor}")
            except Creditor.DoesNotExist:
                # Si no existe, crear uno por defecto
                logger.warning(f"Creditor no encontrado para nombre: {processed_data['creditor']}")
                
                # Crear PostalAddress primero
                postal_address = PostalAddress.objects.create(
                    country="ES",
                    street="Dirección por defecto",
                    city="Ciudad por defecto"
                )
                
                creditor = Creditor.objects.create(
                    name=processed_data["creditor"],
                    address=postal_address
                )
                processed_data["creditor"] = creditor
                logger.debug(f"Creditor creado: {creditor}")

        # Procesar creditor_agent (la API envía el BIC como string, necesitamos el objeto)
        if "creditor_agent" in processed_data and isinstance(processed_data["creditor_agent"], str):
            try:
                creditor_agent = CreditorAgent.objects.get(bic=processed_data["creditor_agent"])
                processed_data["creditor_agent"] = creditor_agent
                logger.debug(f"CreditorAgent encontrado: {creditor_agent}")
            except CreditorAgent.DoesNotExist:
                # Si no existe, crear uno con el BIC proporcionado
                logger.warning(f"CreditorAgent no encontrado para BIC: {processed_data['creditor_agent']}")
                creditor_agent = CreditorAgent.objects.create(
                    bic=processed_data["creditor_agent"],
                    financial_institution_id=f"FIID_{processed_data['creditor_agent']}",
                    other_information=f"Agente creado automáticamente para BIC: {processed_data['creditor_agent']}"
                )
                processed_data["creditor_agent"] = creditor_agent
                logger.debug(f"CreditorAgent creado: {creditor_agent}")
        elif "creditor_agent" not in processed_data:
            # Si no viene creditor_agent, crear uno por defecto
            try:
                creditor_agent = CreditorAgent.objects.first()
                if not creditor_agent:
                    creditor_agent = CreditorAgent.objects.create(
                        bic="DEFAULTBIC",
                        financial_institution_id="DEFAULTFIID",
                        other_information="Agente por defecto"
                    )
                processed_data["creditor_agent"] = creditor_agent
                logger.debug(f"CreditorAgent por defecto asignado: {creditor_agent}")
            except Exception as e:
                logger.error(f"Error al procesar creditor_agent: {e}")
                raise ValidationError(f"Error al procesar creditor_agent: {str(e)}")

        # Procesar payment_identification (la API envía el nombre, necesitamos el objeto)
        if "payment_identification" in processed_data and isinstance(processed_data["payment_identification"], str):
            try:
                payment_identification = PaymentIdentification.objects.get(
                    instruction_id=processed_data["payment_identification"]
                )
                processed_data["payment_identification"] = payment_identification
                logger.debug(f"PaymentIdentification encontrado: {payment_identification}")
            except PaymentIdentification.DoesNotExist:
                # Si no existe, crear uno nuevo
                logger.warning(f"PaymentIdentification no encontrado para instruction_id: {processed_data['payment_identification']}")
                payment_identification = PaymentIdentification.objects.create(
                    end_to_end_id=uuid.uuid4(),
                    instruction_id=processed_data["payment_identification"]
                )
                processed_data["payment_identification"] = payment_identification
                logger.debug(f"PaymentIdentification creado: {payment_identification}")

        # Procesar auth_id si viene como string
        if "auth_id" in processed_data and isinstance(processed_data["auth_id"], str):
            # Convertir a UUID si es necesario
            try:
                if processed_data["auth_id"]:
                    processed_data["auth_id"] = uuid.UUID(processed_data["auth_id"])
            except ValueError:
                # Si no es un UUID válido, generar uno nuevo
                processed_data["auth_id"] = uuid.uuid4()
                logger.warning(f"Auth_id inválido, generado nuevo: {processed_data['auth_id']}")

        # Asegurar que instructed_amount sea Decimal
        if "instructed_amount" in processed_data:
            from decimal import Decimal
            if isinstance(processed_data["instructed_amount"], (int, float)):
                processed_data["instructed_amount"] = Decimal(str(processed_data["instructed_amount"]))

        # Asegurar que requested_execution_date sea Date
        if "requested_execution_date" in processed_data and isinstance(processed_data["requested_execution_date"], str):
            from datetime import datetime
            try:
                processed_data["requested_execution_date"] = datetime.strptime(
                    processed_data["requested_execution_date"], "%Y-%m-%d"
                ).date()
            except ValueError:
                # Si no se puede parsear, usar fecha actual
                processed_data["requested_execution_date"] = timezone.now().date()
                logger.warning(f"Fecha de ejecución inválida, usando fecha actual: {processed_data['requested_execution_date']}")

        logger.debug(f"Datos procesados: {processed_data}")
        return processed_data

    @staticmethod
    @transaction.atomic
    def process_transfer(transfer: Transfer) -> Transfer:
        """Procesa una transferencia existente."""
        try:
            # Verificar fondos
            debtor_account = DebtorAccount.objects.select_for_update().get(
                id=transfer.debtor_account.id
            )
            
            # Validar fondos suficientes
            if debtor_account.balance < transfer.instructed_amount:
                transfer.status = 'RJCT'
                transfer.save()
                LogTransferencia.objects.create(
                    registro=transfer.payment_id,
                    tipo_log='ERROR',
                    contenido='Fondos insuficientes'
                )
                return transfer

            # Validar monedas compatibles
            if debtor_account.currency != transfer.currency:
                transfer.status = 'RJCT'
                transfer.save()
                LogTransferencia.objects.create(
                    registro=transfer.payment_id,
                    tipo_log='ERROR',
                    contenido='Moneda incompatible'
                )
                return transfer

            # Crear movimiento de débito (esto actualizará el saldo automáticamente)
            AccountMovement.objects.create(
                account=debtor_account,
                tipo=AccountMovement.PAYMENT,
                monto=transfer.instructed_amount
            )

            # Si es una transferencia interna, buscar la cuenta deudora correspondiente
            creditor_account = transfer.creditor_account
            if creditor_account:
                try:
                    # Buscar la cuenta deudora correspondiente por IBAN
                    destino_account = DebtorAccount.objects.select_for_update().get(
                        iban=creditor_account.iban
                    )
                    # Crear movimiento de crédito (esto actualizará el saldo automáticamente)
                    AccountMovement.objects.create(
                        account=destino_account,
                        tipo=AccountMovement.DEPOSIT,
                        monto=transfer.instructed_amount
                    )
                except DebtorAccount.DoesNotExist:
                    logger.warning(f"No se encontró cuenta deudora para el IBAN: {creditor_account.iban}")

            transfer.status = 'ACSC'
            transfer.save()
            
            LogTransferencia.objects.create(
                registro=transfer.payment_id,
                tipo_log='TRANSFER',
                contenido=f'Transferencia completada: {transfer.instructed_amount} {transfer.currency}'
            )

        except Exception as e:
            logger.error(f"Error al procesar transferencia {transfer.payment_id}: {str(e)}")
            logger.error(traceback.format_exc())
            
            transfer.status = 'RJCT'
            transfer.save()
            LogTransferencia.objects.create(
                registro=transfer.payment_id,
                tipo_log='ERROR',
                contenido=f'Error al procesar la transferencia: {str(e)}'
            )

        return transfer

    @staticmethod
    def confirm_transfer(payment_id: str, otp_input: str, auth_id: str = None) -> Dict[str, Any]:
        """
        Confirma una transferencia con OTP.
        Recibe los mismos parámetros que envía send_transfer:
        - payment_id: str - ID de la transferencia
        - otp_input: str - Código OTP para confirmar
        - auth_id: str - ID del usuario autorizador (opcional)
        """
        with transaction.atomic():
            try:
                # Buscar el challenge OTP
                challenge = OTPChallenge.objects.select_for_update().get(
                    payment_id=payment_id, 
                    otp=otp_input, 
                    status="CREATED"
                )
                challenge.status = "CONFIRMED"
                if auth_id:
                    challenge.auth_id = auth_id
                challenge.save()

                # Actualizar la transferencia
                transfer = Transfer.objects.select_for_update().get(payment_id=payment_id)
                transfer.status = "ACCP"
                if auth_id:
                    transfer.auth_id = auth_id
                transfer.save()

                # Procesar la transferencia
                transfer = TransferService.process_transfer(transfer)

                logger.info(f"Transferencia {payment_id} confirmada exitosamente con OTP")

                return {
                    "payment_id": payment_id,
                    "status": transfer.status,
                    "timestamp": timezone.now().isoformat(),
                    "auth_id": auth_id or transfer.auth_id
                }
                
            except OTPChallenge.DoesNotExist:
                logger.error(f"OTP Challenge no encontrado para payment_id: {payment_id}, OTP: {otp_input}")
                return {
                    "payment_id": payment_id,
                    "status": "RJCT",
                    "error": "OTP inválido o expirado",
                    "timestamp": timezone.now().isoformat()
                }
            except Transfer.DoesNotExist:
                logger.error(f"Transferencia no encontrada para payment_id: {payment_id}")
                return {
                    "payment_id": payment_id,
                    "status": "RJCT",
                    "error": "Transferencia no encontrada",
                    "timestamp": timezone.now().isoformat()
                }
            except Exception as e:
                logger.error(f"Error al confirmar transferencia {payment_id}: {str(e)}")
                return {
                    "payment_id": payment_id,
                    "status": "RJCT",
                    "error": f"Error interno: {str(e)}",
                    "timestamp": timezone.now().isoformat()
                }

    @staticmethod
    def confirm_transfer_with_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Confirma una transferencia recibiendo el payload completo de la API.
        Este método recibe exactamente los mismos datos que envía send_transfer.
        
        Args:
            payload: Dict con los datos de la transferencia incluyendo payment_id y auth_id
            
        Returns:
            Dict con la respuesta de confirmación
        """
        logger.debug(f"Confirmando transferencia con payload: {payload}")
        
        try:
            payment_id = payload.get("payment_id")
            auth_id = payload.get("auth_id")
            
            if not payment_id:
                return {
                    "status": "RJCT",
                    "error": "payment_id es requerido",
                    "timestamp": timezone.now().isoformat()
                }
            
            # Buscar la transferencia existente
            try:
                transfer = Transfer.objects.get(payment_id=payment_id)
                logger.debug(f"Transferencia encontrada: {transfer.payment_id} con status: {transfer.status}")
            except Transfer.DoesNotExist:
                return {
                    "payment_id": payment_id,
                    "status": "RJCT",
                    "error": "Transferencia no encontrada",
                    "timestamp": timezone.now().isoformat()
                }
            
            # Si la transferencia ya está procesada, devolver su estado actual
            if transfer.status in ['ACSC', 'RJCT']:
                return {
                    "payment_id": payment_id,
                    "status": transfer.status,
                    "timestamp": timezone.now().isoformat(),
                    "auth_id": auth_id or transfer.auth_id
                }
            
            # Buscar el OTP challenge más reciente para esta transferencia
            try:
                otp_challenge = OTPChallenge.objects.filter(
                    payment_id=payment_id,
                    status="CREATED"
                ).latest('created_at')
                
                # Confirmar la transferencia con el OTP
                return TransferService.confirm_transfer(
                    payment_id=payment_id,
                    otp_input=otp_challenge.otp,
                    auth_id=auth_id
                )
                
            except OTPChallenge.DoesNotExist:
                # Si no hay OTP challenge, procesar directamente
                logger.warning(f"No se encontró OTP challenge para payment_id: {payment_id}, procesando directamente")
                
                with transaction.atomic():
                    transfer.status = "ACCP"
                    if auth_id:
                        transfer.auth_id = auth_id
                    transfer.save()
                    
                    # Procesar la transferencia
                    transfer = TransferService.process_transfer(transfer)
                    
                    return {
                        "payment_id": payment_id,
                        "status": transfer.status,
                        "timestamp": timezone.now().isoformat(),
                        "auth_id": auth_id or transfer.auth_id
                    }
                    
        except Exception as e:
            logger.error(f"Error en confirm_transfer_with_payload: {str(e)}")
            return {
                "payment_id": payload.get("payment_id"),
                "status": "RJCT",
                "error": f"Error interno: {str(e)}",
                "timestamp": timezone.now().isoformat()
            }
