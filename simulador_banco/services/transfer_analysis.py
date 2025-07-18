import openai
from decimal import Decimal
from typing import Dict, List
from django.conf import settings
from banco.models import Transfer, AccountMovement, LogTransferencia

class TransferAnalysisService:
    RISK_LEVELS = {
        'LOW': 'BAJO',
        'MEDIUM': 'MEDIO',
        'HIGH': 'ALTO',
        'CRITICAL': 'CRÍTICO'
    }
    
    @classmethod
    def analyze_transfer(cls, transfer: Transfer) -> Dict:
        """
        Analiza una transferencia usando GPT-4 para detectar patrones sospechosos.
        
        Args:
            transfer: Objeto Transfer a analizar
            
        Returns:
            Dict con resultados del análisis
        """
        # Obtener historial de transferencias del deudor
        recent_transfers = Transfer.objects.filter(
            debtor=transfer.debtor
        ).order_by('-requested_execution_date')[:10]
        
        # Obtener movimientos recientes
        recent_movements = AccountMovement.objects.filter(
            account=transfer.debtor_account
        ).order_by('-fecha')[:10]
        
        # Construir prompt para GPT-4
        prompt = cls._build_analysis_prompt(transfer, recent_transfers, recent_movements)
        
        try:
            # Llamar a GPT-4
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{
                    "role": "system",
                    "content": """Eres un analista experto en detección de fraudes bancarios.
                    Tu tarea es analizar transferencias y detectar patrones sospechosos.
                    Debes responder en formato JSON con los siguientes campos:
                    {
                        "risk_level": "LOW|MEDIUM|HIGH|CRITICAL",
                        "risk_factors": ["lista de factores de riesgo"],
                        "recommendations": ["lista de recomendaciones"],
                        "explanation": "explicación detallada del análisis"
                    }"""
                }, {
                    "role": "user",
                    "content": prompt
                }]
            )
            
            # Parsear respuesta
            analysis = response.choices[0].message.content
            
            # Registrar análisis
            LogTransferencia.objects.create(
                registro=transfer.payment_id,
                tipo_log='AML',
                contenido=analysis
            )
            
            return analysis
            
        except Exception as e:
            # Registrar error
            LogTransferencia.objects.create(
                registro=transfer.payment_id,
                tipo_log='ERROR',
                contenido=f'Error en análisis GPT: {str(e)}'
            )
            return {
                'risk_level': 'HIGH',
                'risk_factors': ['Error en análisis automático'],
                'recommendations': ['Revisar manualmente'],
                'explanation': f'Error al analizar: {str(e)}'
            }
    
    @classmethod
    def _build_analysis_prompt(
        cls,
        transfer: Transfer,
        recent_transfers: List[Transfer],
        recent_movements: List[AccountMovement]
    ) -> str:
        """Construye el prompt para GPT-4."""
        prompt = f"""
        TRANSFERENCIA ACTUAL:
        - ID: {transfer.payment_id}
        - Monto: {transfer.instructed_amount} {transfer.currency}
        - Origen: {transfer.debtor.name} ({transfer.debtor_account.iban})
        - Destino: {transfer.creditor.name} ({transfer.creditor_account.iban})
        - Fecha: {transfer.requested_execution_date}
        
        TRANSFERENCIAS RECIENTES:
        {cls._format_transfers(recent_transfers)}
        
        MOVIMIENTOS RECIENTES:
        {cls._format_movements(recent_movements)}
        
        Analiza esta transferencia y detecta posibles patrones sospechosos.
        Considera:
        1. Montos inusuales
        2. Frecuencia de transferencias
        3. Patrones de comportamiento
        4. Destinatarios nuevos o inusuales
        5. Horarios de operación
        """
        return prompt
    
    @staticmethod
    def _format_transfers(transfers: List[Transfer]) -> str:
        """Formatea lista de transferencias para el prompt."""
        result = []
        for t in transfers:
            result.append(
                f"- {t.requested_execution_date}: "
                f"{t.instructed_amount} {t.currency} "
                f"a {t.creditor.name}"
            )
        return "\n".join(result)
    
    @staticmethod
    def _format_movements(movements: List[AccountMovement]) -> str:
        """Formatea lista de movimientos para el prompt."""
        result = []
        for m in movements:
            result.append(
                f"- {m.fecha}: {m.tipo} - {m.monto} "
                f"({m.descripcion[:50]}...)"
            )
        return "\n".join(result) 