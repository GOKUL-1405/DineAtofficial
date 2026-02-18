"""
UPI QR Code Generation Utility for DineAt Restaurant
"""
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings
import os

class UPIQRGenerator:
    """Generate UPI QR codes for payments"""
    
    def __init__(self, upi_id="gokulkumar1406@okaxis", merchant_name="DineAt Restaurant"):
        self.upi_id = upi_id
        self.merchant_name = merchant_name
        self.transaction_note = "DineAt Food Order"
    
    def generate_upi_string(self, amount=None, order_id=None):
        """
        Generate UPI payment string
        Format: upi://pay?pa=upi_id&pn=merchant_name&am=amount&cu=INR&tn=transaction_note
        """
        upi_url = f"upi://pay?pa={self.upi_id}&pn={self.merchant_name}"
        
        if amount:
            upi_url += f"&am={amount}&cu=INR"
        
        if order_id:
            note = f"{self.transaction_note} - Order #{order_id}"
        else:
            note = self.transaction_note
        
        upi_url += f"&tn={note}"
        
        return upi_url
    
    def generate_qr_code(self, amount=None, order_id=None, size=10, border=2):
        """
        Generate QR code image for UPI payment
        
        Args:
            amount (float): Payment amount
            order_id (int): Order ID
            size (int): QR code size
            border (int): QR code border size
        
        Returns:
            BytesIO: QR code image data
        """
        upi_string = self.generate_upi_string(amount, order_id)
        
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size,
            border=border,
        )
        
        qr.add_data(upi_string)
        qr.make(fit=True)
        
        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to BytesIO
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        
        return buffer
    
    def save_qr_code(self, amount=None, order_id=None, filename=None):
        """
        Save QR code to media directory
        
        Args:
            amount (float): Payment amount
            order_id (int): Order ID
            filename (str): Custom filename
        
        Returns:
            str: Relative path to saved QR code
        """
        if not filename:
            if order_id:
                filename = f"upi_qr_order_{order_id}.png"
            else:
                filename = f"upi_qr_generic.png"
        
        # Generate QR code
        qr_buffer = self.generate_qr_code(amount, order_id)
        
        # Create media directory if it doesn't exist
        media_dir = os.path.join(settings.MEDIA_ROOT, 'upi_qr_codes')
        os.makedirs(media_dir, exist_ok=True)
        
        # Save QR code
        file_path = os.path.join(media_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(qr_buffer.getvalue())
        
        # Return relative path
        return f"upi_qr_codes/{filename}"
    
    def get_upi_deep_link(self, amount=None, order_id=None):
        """
        Get UPI deep link for sharing
        
        Args:
            amount (float): Payment amount
            order_id (int): Order ID
        
        Returns:
            str: UPI deep link
        """
        return self.generate_upi_string(amount, order_id)
    
    def generate_payment_details(self, amount, order_id):
        """
        Generate complete payment details for display
        
        Args:
            amount (float): Payment amount
            order_id (int): Order ID
        
        Returns:
            dict: Payment details
        """
        return {
            'upi_id': self.upi_id,
            'merchant_name': self.merchant_name,
            'amount': amount,
            'order_id': order_id,
            'transaction_note': f"{self.transaction_note} - Order #{order_id}",
            'upi_string': self.generate_upi_string(amount, order_id),
            'qr_code_path': self.save_qr_code(amount, order_id),
            'deep_link': self.get_upi_deep_link(amount, order_id)
        }

def create_upi_payment_qr(amount, order_id):
    """
    Helper function to create UPI payment QR code
    
    Args:
        amount (float): Payment amount
        order_id (int): Order ID
    
    Returns:
        dict: Payment details with QR code
    """
    generator = UPIQRGenerator()
    return generator.generate_payment_details(amount, order_id)

def get_upi_payment_info(amount, order_id):
    """
    Get UPI payment information without generating QR
    
    Args:
        amount (float): Payment amount
        order_id (int): Order ID
    
    Returns:
        dict: Payment information
    """
    generator = UPIQRGenerator()
    return {
        'upi_id': generator.upi_id,
        'merchant_name': generator.merchant_name,
        'amount': amount,
        'order_id': order_id,
        'transaction_note': f"{generator.transaction_note} - Order #{order_id}",
        'upi_string': generator.generate_upi_string(amount, order_id),
        'deep_link': generator.get_upi_deep_link(amount, order_id)
    }
