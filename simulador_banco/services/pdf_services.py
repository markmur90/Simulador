"""
Servicio para la generación de PDFs del simulador bancario.
Incluye generación de estados de cuenta y comprobantes de transferencia.
"""

import os
from io import BytesIO
from datetime import datetime
from typing import List, Dict, Any, Optional

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, Flowable, PageTemplate, Frame
)
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _

class WaterMark(Flowable):
    """Clase para crear marcas de agua en los PDFs."""
    def __init__(self, text="CONFIDENCIAL", angle=45):
        Flowable.__init__(self)
        self.text = text
        self.angle = angle
        
    def draw(self):
        canvas = self.canv
        canvas.saveState()
        canvas.setFont('Helvetica', 70)
        canvas.setFillColor(colors.grey)
        canvas.setFillAlpha(0.1)
        canvas.translate(A4[0]/2, A4[1]/2)
        canvas.rotate(self.angle)
        canvas.drawCentredString(0, 0, self.text)
        canvas.restoreState()

class PDFService:
    """Servicio principal para generación de PDFs."""
    
    def __init__(self, page_size='A4', language='es'):
        """
        Inicializa el servicio de PDF.
        
        Args:
            page_size: 'A4' o 'letter'
            language: Código de idioma ('es', 'en')
        """
        self.page_size = A4 if page_size == 'A4' else letter
        self.language = language
        self.styles = getSampleStyleSheet()
        self._setup_styles()
        
    def _setup_styles(self):
        """Configura los estilos personalizados para los PDFs."""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1  # Centrado
        )
        
        self.subtitle_style = ParagraphStyle(
            'CustomSubTitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceAfter=20,
            alignment=1
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=12
        )
        
        self.footer_style = ParagraphStyle(
            'CustomFooter',
            parent=self.styles['Normal'],
            fontSize=8,
            textColor=colors.grey
        )

    def _add_header(self, canvas, doc):
        """Agrega el encabezado al PDF."""
        canvas.saveState()
        # Logo
        logo_path = os.path.join(settings.STATIC_ROOT, 'img/mi-logo.png')
        if os.path.exists(logo_path):
            canvas.drawImage(logo_path, 40, doc.pagesize[1]-60, width=120, height=40)
        
        # Fecha y hora
        canvas.setFont('Helvetica', 8)
        canvas.drawRightString(
            doc.pagesize[0]-40, 
            doc.pagesize[1]-20,
            timezone.now().strftime("%d/%m/%Y %H:%M:%S")
        )
        
        # Número de página
        canvas.drawRightString(
            doc.pagesize[0]-40,
            30,
            f'Página {canvas.getPageNumber()}'
        )
        canvas.restoreState()

    def _add_footer(self, canvas, doc):
        """Agrega el pie de página al PDF."""
        canvas.saveState()
        canvas.setFont('Helvetica', 8)
        footer_text = _(
            "Este documento es una representación digital de una transacción bancaria. "
            "Para verificar su autenticidad, escanee el código QR o visite nuestra página web."
        )
        canvas.drawString(40, 40, footer_text)
        canvas.restoreState()

    def _create_qr(self, data: str, size: int = 100) -> Drawing:
        """Crea un código QR."""
        qr = QrCodeWidget(data)
        bounds = qr.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        drawing = Drawing(size, size, transform=[size/width, 0, 0, size/height, 0, 0])
        drawing.add(qr)
        return drawing

    def generate_account_statement(
        self,
        account: Any,
        movements: List[Any],
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        is_creditor: bool = False
    ) -> BytesIO:
        """
        Genera el estado de cuenta en PDF.
        
        Args:
            account: Objeto DebtorAccount o CreditorAccount
            movements: Lista de movimientos o transferencias
            start_date: Fecha inicial del periodo
            end_date: Fecha final del periodo
            is_creditor: True si es una cuenta de acreedor, False si es de deudor
        
        Returns:
            BytesIO con el PDF generado
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=self.page_size,
            rightMargin=40,
            leftMargin=40,
            topMargin=60,
            bottomMargin=60
        )
        
        elements = []
        
        # Título
        elements.append(Paragraph(_("Estado de Cuenta"), self.title_style))
        elements.append(Spacer(1, 20))
        
        # Información de la cuenta
        account_info = [
            [_("Titular"), account.creditor.name if is_creditor else account.debtor.name],
            [_("IBAN"), account.iban],
            [_("Tipo de Cuenta"), _("Cuenta Acreedora") if is_creditor else _("Cuenta Deudora")],
            [_("Moneda"), account.currency],
            [_("Periodo"), f"{start_date:%d/%m/%Y} - {end_date:%d/%m/%Y}" if start_date and end_date else _("Completo")],
        ]
        
        account_table = Table(account_info, colWidths=[120, 350])
        account_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(account_table)
        elements.append(Spacer(1, 20))
        
        # Resumen de movimientos
        elements.append(Paragraph(_("Resumen de Movimientos"), self.subtitle_style))
        
        if is_creditor:
            # Para acreedores, los movimientos son transferencias
            total_received = sum(m.instructed_amount for m in movements if m.status == 'ACSC')
            summary_data = [
                [_("Total Recibido"), f"{account.currency} {total_received:,.2f}"],
                [_("Saldo Actual"), f"{account.currency} {account.balance:,.2f}"],
            ]
        else:
            # Para deudores, los movimientos son AccountMovement
            total_deposits = sum(m.monto for m in movements if m.tipo == 'DEPOSIT')
            total_payments = sum(m.monto for m in movements if m.tipo == 'PAYMENT')
            summary_data = [
                [_("Total Depósitos"), f"{account.currency} {total_deposits:,.2f}"],
                [_("Total Pagos"), f"{account.currency} {total_payments:,.2f}"],
                [_("Saldo Actual"), f"{account.currency} {account.balance:,.2f}"],
            ]
        
        summary_table = Table(summary_data, colWidths=[120, 350])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 20))
        
        # Detalle de movimientos
        elements.append(Paragraph(_("Detalle de Movimientos"), self.subtitle_style))
        
        if is_creditor:
            # Encabezados para transferencias
            movements_data = [[
                _("Fecha"),
                _("Estado"),
                _("Ordenante"),
                _("Monto"),
                _("Concepto")
            ]]
            
            # Datos de transferencias
            for mov in movements:
                movements_data.append([
                    mov.created_at.strftime("%d/%m/%Y %H:%M"),
                    mov.get_status_display(),
                    mov.debtor.name,
                    f"{account.currency} {mov.instructed_amount:,.2f}",
                    mov.remittance_information_unstructured or ''
                ])
        else:
            # Encabezados para movimientos de cuenta
            movements_data = [[
                _("Fecha"),
                _("Tipo"),
                _("Descripción"),
                _("Monto"),
                _("Saldo")
            ]]
            
            # Datos de movimientos
            running_balance = 0
            for mov in movements:
                if mov.tipo == 'DEPOSIT':
                    running_balance += mov.monto
                else:
                    running_balance -= mov.monto
                    
                movements_data.append([
                    mov.fecha.strftime("%d/%m/%Y %H:%M"),
                    mov.get_tipo_display(),
                    mov.descripcion if hasattr(mov, 'descripcion') else '',
                    f"{account.currency} {mov.monto:,.2f}",
                    f"{account.currency} {running_balance:,.2f}"
                ])
        
        movements_table = Table(movements_data, colWidths=[80, 70, 200, 80, 80])
        movements_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (-2, 0), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        elements.append(movements_table)
        
        # Agregar marca de agua
        elements.append(WaterMark())
        
        # Agregar código QR
        qr_data = f"account={account.iban}&date={timezone.now().isoformat()}"
        qr = self._create_qr(qr_data)
        elements.append(Spacer(1, 20))
        elements.append(renderPDF.draw(qr, doc))
        
        # Construir el PDF
        doc.build(
            elements,
            onFirstPage=self._add_header,
            onLaterPages=self._add_header,
            onLastPage=self._add_footer
        )
        
        buffer.seek(0)
        return buffer

    def generate_transfer_receipt(self, transfer: Any) -> BytesIO:
        """
        Genera el comprobante de transferencia en PDF.
        
        Args:
            transfer: Objeto Transfer
        
        Returns:
            BytesIO con el PDF generado
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=self.page_size,
            rightMargin=40,
            leftMargin=40,
            topMargin=60,
            bottomMargin=60
        )
        
        elements = []
        
        # Título
        elements.append(Paragraph(_("Comprobante de Transferencia"), self.title_style))
        elements.append(Spacer(1, 20))
        
        # Datos de la transferencia
        transfer_data = [
            [_("ID de Pago"), transfer.payment_id],
            [_("Estado"), transfer.get_status_display()],
            [_("Fecha"), transfer.created_at.strftime("%d/%m/%Y %H:%M:%S")],
            [_("Monto"), f"{transfer.instructed_amount} {transfer.currency}"],
            [_("Cuenta Origen"), transfer.debtor_account.iban],
            [_("Titular Origen"), transfer.debtor.name],
            [_("Cuenta Destino"), transfer.creditor_account.iban],
            [_("Titular Destino"), transfer.creditor.name],
            [_("Concepto"), transfer.remittance_information_unstructured or ""],
            [_("Número de Autorización"), str(transfer.auth_id or '')],
        ]
        
        transfer_table = Table(transfer_data, colWidths=[150, 350])
        transfer_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(transfer_table)
        elements.append(Spacer(1, 20))
        
        # Términos y condiciones
        elements.append(Paragraph(_("Términos y Condiciones"), self.subtitle_style))
        terms_text = _("""
        1. Este comprobante es válido como prueba de la transferencia realizada.
        2. La transferencia está sujeta a verificación y puede ser reversada en caso de error o fraude.
        3. El banco no se hace responsable por errores en los datos proporcionados por el cliente.
        4. Para cualquier reclamo, conserve este comprobante.
        5. La transferencia se considera definitiva una vez que aparezca en el estado de cuenta del beneficiario.
        """)
        elements.append(Paragraph(terms_text, self.normal_style))
        
        # Agregar marca de agua
        elements.append(WaterMark(_("COMPROBANTE VÁLIDO")))
        
        # Agregar código QR con datos de verificación
        qr_data = (
            f"transfer_id={transfer.payment_id}&"
            f"amount={transfer.instructed_amount}&"
            f"currency={transfer.currency}&"
            f"date={transfer.created_at.isoformat()}"
        )
        qr = self._create_qr(qr_data)
        elements.append(Spacer(1, 20))
        elements.append(renderPDF.draw(qr, doc))
        
        # Construir el PDF
        doc.build(
            elements,
            onFirstPage=self._add_header,
            onLaterPages=self._add_header,
            onLastPage=self._add_footer
        )
        
        buffer.seek(0)
        return buffer 