import flet as ft
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl
import threading
import socket



class EmailService:
    def __init__(self):
        # CONFIGURACIÓN DE EMAIL 
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "soporte.coflita@gmail.com"  
        self.sender_password = "lvfg cbgq lfnu hlig"  
        # Modo de prueba - cambia a False para envío real
        self.test_mode = False  # Cambiado a False para envío real
        
        # Configuraciones SSL alternativas
        self.ssl_methods = [
            "default",      # Configuración SSL por defecto
            "unverified",   # SSL sin verificación (solo para desarrollo)
            "legacy",       # Configuración SSL legacy
            "no_ssl"        # Sin SSL (puerto 25, menos seguro)
        ]
        self.current_ssl_method = 1

    def create_booking_email_html(self, guest_name, room_name, check_in, check_out, nights, total_price, booking_id):
        """Crea el HTML del email de confirmación de reserva"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #1A237E; color: white; padding: 20px; text-align: center; }}
                .content {{ background-color: #f9f9f9; padding: 20px; }}
                .booking-details {{ background-color: white; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .footer {{ background-color: #333; color: white; padding: 15px; text-align: center; }}
                .highlight {{ color: #FFA000; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏨 Hotel Coflita</h1>
                    <h2>Confirmación de Reserva</h2>
                </div>
                
                <div class="content">
                    <h3>¡Hola {guest_name}!</h3>
                    <p>Nos complace confirmar tu reserva en Hotel Coflita. A continuación encontrarás los detalles:</p>
                    
                    <div class="booking-details">
                        <h4>📋 Detalles de la Reserva</h4>
                        <p><strong>Número de Reserva:</strong> <span class="highlight">#{booking_id:04d}</span></p>
                        <p><strong>Número de Habitacion:</strong> <span class="highlight">#{booking_id:04d}</span></p>
                        <p><strong>Huésped:</strong> {guest_name}</p>
                        <p><strong>Habitación:</strong> {room_name}</p>
                        <p><strong>Check-in:</strong> {check_in.strftime('%d/%m/%Y')}</p>
                        <p><strong>Check-out:</strong> {check_out.strftime('%d/%m/%Y')}</p>
                        <p><strong>Noches:</strong> {nights}</p>
                        <p><strong>Total:</strong> <span class="highlight">${total_price}</span></p>
                    </div>
                    
                    <div class="booking-details">
                        <h4>📍 Información Importante</h4>
                        <p><strong>Check-in:</strong> A partir de las 15:00 hrs</p>
                        <p><strong>Check-out:</strong> Hasta las 12:00 hrs</p>
                        <p><strong>Dirección:</strong> Av. Duarte Quiros 1205, Cordoba Capital, Argentina</p>
                        <p><strong>Teléfono:</strong> +54 351 237-9493</p>
                    </div>
                    
                    <p>¡Esperamos verte pronto en Hotel Coflita!</p>
                </div>
                
                <div class="footer">
                    <p>Hotel Coflita - Tu destino perfecto para descansar</p>
                    <p>📧 soporte.coflita@gmail.com | 📞 +54 351 237-9493</p>
                    <p>Nuestro Instagram: coflita2.4 <p>
                </div>
            </div>
        </body>
        </html>
        """
        return html

    def create_contact_email_html(self, contact_name, contact_email, contact_phone, contact_message):
        """Crea el HTML del email de confirmación de contacto"""
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #1A237E; color: white; padding: 20px; text-align: center; }}
                .content {{ background-color: #f9f9f9; padding: 20px; }}
                .contact-details {{ background-color: white; padding: 15px; margin: 10px 0; border-radius: 5px; }}
                .footer {{ background-color: #333; color: white; padding: 15px; text-align: center; }}
                .highlight {{ color: #FFA000; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🏨 Hotel Coflita</h1>
                    <h2>Confirmación de Consulta</h2>
                </div>
                
                <div class="content">
                    <h3>¡Hola {contact_name}!</h3>
                    <p>Hemos recibido tu consulta y nos pondremos en contacto contigo lo antes posible.</p>
                    
                    <div class="contact-details">
                        <h4>📋 Detalles de tu Consulta</h4>
                        <p><strong>Nombre:</strong> {contact_name}</p>
                        <p><strong>Email:</strong> {contact_email}</p>
                        <p><strong>Teléfono:</strong> {contact_phone}</p>
                        <p><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                    </div>
                    
                    <div class="contact-details">
                        <h4>💬 Tu Mensaje</h4>
                        <p style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">{contact_message}</p>
                    </div>
                    
                    <div class="contact-details">
                        <h4>⏰ Tiempo de Respuesta</h4>
                        <p>Nuestro equipo te responderá en un plazo de <span class="highlight">24-48 horas</span>.</p>
                        <p>Si tu consulta es urgente, puedes contactarnos directamente al +123 456 7890.</p>
                    </div>
                    
                    <p>¡Gracias por contactar con Hotel Coflita!</p>
                </div>
                
                <div class="footer">
                    <p>Hotel Coflita - Tu destino perfecto para descansar</p>
                    <p>📧 info@hotelcoflita.com | 📞 +123 456 7890</p>
                </div>
            </div>
        </body>
        </html>
        """
        return html

    def send_email(self, to_email, subject, html_content):
        """Método genérico para enviar emails"""
        try:
            # Crear mensaje
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = to_email
            
            # Crear parte HTML
            html_part = MIMEText(html_content, "html", "utf-8")
            message.attach(html_part)
            
            # Crear contexto SSL seguro
            context = ssl.create_default_context()
            
            # Conectar al servidor y enviar email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, message.as_string())
            
            print(f"✅ Email enviado exitosamente a {to_email}")
            return True, "Email enviado exitosamente"
            
        except smtplib.SMTPAuthenticationError:
            error_msg = "Error de autenticación: Verifica el email y contraseña"
            print(f"❌ {error_msg}")
            return False, error_msg
            
        except smtplib.SMTPRecipientsRefused:
            error_msg = "Email de destinatario inválido"
            print(f"❌ {error_msg}")
            return False, error_msg
            
        except smtplib.SMTPServerDisconnected:
            error_msg = "Conexión perdida con el servidor SMTP"
            print(f"❌ {error_msg}")
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Error inesperado al enviar email: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg

    def send_booking_confirmation(self, guest_email, guest_name, room_name, check_in, check_out, nights, total_price, booking_id):
        """Envía el email de confirmación de reserva"""
        
        # Si está en modo de prueba, simular envío
        if self.test_mode:
            print("🧪 MODO DE PRUEBA ACTIVADO")
            print(f"📧 Email que se enviaría a: {guest_email}")
            print(f"👤 Huésped: {guest_name}")
            print(f"🏨 Habitación: {room_name}")
            print(f"📅 Check-in: {check_in.strftime('%d/%m/%Y')}")
            print(f"📅 Check-out: {check_out.strftime('%d/%m/%Y')}")
            print(f"🌙 Noches: {nights}")
            print(f"💰 Total: ${total_price}")
            print(f"🔢 Reserva #: {booking_id:04d}")
            print(f"🔢 Habitacion #: {booking_id:04d}")
            print("✅ Email simulado enviado exitosamente")
            return True, "Email enviado en modo de prueba"
        
        # Envío real
        subject = f"Confirmación de Reserva #{booking_id:04d} - Hotel Coflita"
        html_content = self.create_booking_email_html(
            guest_name, room_name, check_in, check_out, nights, total_price, booking_id
        )
        
        return self.send_email(guest_email, subject, html_content)

    def send_contact_confirmation(self, contact_name, contact_email, contact_phone, contact_message):
        """Envía el email de confirmación de consulta"""
        
        # Si está en modo de prueba, simular envío
        if self.test_mode:
            print("🧪 MODO DE PRUEBA - EMAIL DE CONFIRMACIÓN DE CONSULTA")
            print(f"📧 Email que se enviaría a: {contact_email}")
            print(f"👤 Nombre: {contact_name}")
            print(f"📱 Teléfono: {contact_phone}")
            print(f"💬 Mensaje: {contact_message}")
            print("✅ Email de confirmación simulado enviado exitosamente")
            return True, "Email de confirmación enviado en modo de prueba"
        
        # Envío real
        subject = "Confirmación de Consulta - Hotel Coflita"
        html_content = self.create_contact_email_html(
            contact_name, contact_email, contact_phone, contact_message
        )
        
        # Enviar email de confirmación al cliente
        success, message = self.send_email(contact_email, subject, html_content)
        
        if success:
            # También enviar copia al hotel (opcional)
            try:
                hotel_subject = f"Nueva Consulta de {contact_name}"
                hotel_html = f"""
                <h2>Nueva Consulta Recibida</h2>
                <p><strong>Nombre:</strong> {contact_name}</p>
                <p><strong>Email:</strong> {contact_email}</p>
                <p><strong>Teléfono:</strong> {contact_phone}</p>
                <p><strong>Mensaje:</strong></p>
                <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">
                    {contact_message}
                </div>
                <p><strong>Fecha:</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
                """
                
                # Enviar al email del hotel (puedes cambiar esta dirección)
                hotel_email = "soporte.coflita@gmail.com"  # Cambia por el email real del hotel
                self.send_email(hotel_email, hotel_subject, hotel_html)
                
            except Exception as e:
                print(f"⚠️ No se pudo enviar copia al hotel: {e}")
        
        return success, message

    def toggle_test_mode(self):
        """Alterna entre modo de prueba y modo real"""
        self.test_mode = not self.test_mode
        mode = "PRUEBA" if self.test_mode else "REAL"
        print(f"🔄 Modo cambiado a: {mode}")
        return self.test_mode

class CarRentalService:
    def __init__(self):
        self.cars = [
            {
                "id": 1,
                "name": "Toyota Corolla",
                "category": "Económico",
                "price_per_day": 45,
                "capacity": 5,
                "transmission": "Automático",
                "fuel": "Gasolina",
                "features": ["Aire Acondicionado", "Radio", "Bluetooth"],
                "image": "corolla.jpg"
            },
            {
                "id": 2,
                "name": "Honda CR-V",
                "category": "SUV",
                "price_per_day": 75,
                "capacity": 7,
                "transmission": "Automático",
                "fuel": "Gasolina",
                "features": ["Aire Acondicionado", "GPS", "Bluetooth", "Cámara Trasera"],
                "image": "crv.jpg"
            },
            {
                "id": 3,
                "name": "BMW Serie 3",
                "category": "Lujo",
                "price_per_day": 120,
                "capacity": 5,
                "transmission": "Automático",
                "fuel": "Gasolina Premium",
                "features": ["Aire Acondicionado", "GPS", "Bluetooth", "Asientos de Cuero", "Techo Solar"],
                "image": "bmw3.jpg"
            },
            {
                "id": 4,
                "name": "Ford Transit",
                "category": "Van",
                "price_per_day": 90,
                "capacity": 12,
                "transmission": "Manual",
                "fuel": "Diesel",
                "features": ["Aire Acondicionado", "Radio", "Amplio Espacio"],
                "image": "transit.jpg"
            }
        ]
        self.rentals = []

    def get_car(self, car_id):
        for car in self.cars:
            if car["id"] == car_id:
                return car
        return None

    def create_rental(self, car_id, customer_name, customer_email, pickup_date, return_date):
        rental_id = len(self.rentals) + 1
        rental = {
            "id": rental_id,
            "car_id": car_id,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "pickup_date": pickup_date,
            "return_date": return_date,
            "created_at": datetime.now()
        }
        self.rentals.append(rental)
        return rental_id

class Servicio_a_la_habitacion:
    def __init__(self):
        self.menu_categories = {
            "Desayunos": [
                {"id": 1, "name": "Desayuno Continental", "price": 15, "description": "Pan tostado, mermelada, café y jugo"},
                {"id": 2, "name": "Desayuno Americano", "price": 22, "description": "Huevos, tocino, salchichas, pan tostado y café"},
                {"id": 3, "name": "Desayuno Saludable", "price": 18, "description": "Yogurt, granola, frutas frescas y té verde"}
            ],
            "Almuerzos": [
                {"id": 4, "name": "Ensalada César", "price": 16, "description": "Lechuga, pollo, crutones, queso parmesano"},
                {"id": 5, "name": "Pasta Alfredo", "price": 20, "description": "Pasta con salsa cremosa y pollo"},
                {"id": 6, "name": "Salmón Grillado", "price": 28, "description": "Salmón con vegetales y arroz"}
            ],
            "Cenas": [
                {"id": 7, "name": "Filete de Res", "price": 25, "description": "Filete con papas y ensalada"},
                {"id": 8, "name": "Pollo a la Parrilla", "price": 25, "description": "Pollo con vegetales asados"},
                {"id": 9, "name": "Paella de Mariscos", "price": 32, "description": "Arroz con mariscos frescos"}
            ],
            "Bebidas": [
                {"id": 10, "name": "Vino Tinto", "price": 8, "description": "Copa de vino tinto de la casa"},
                {"id": 11, "name": "Cerveza", "price": 5, "description": "Cerveza nacional fría"},
                {"id": 12, "name": "Jugo Natural", "price": 4, "description": "Jugo de frutas frescas"}
            ],
            "Postres": [
                {"id": 13, "name": "Tiramisu", "price": 12, "description": "Postre italiano tradicional"},
                {"id": 14, "name": "Cheesecake", "price": 10, "description": "Tarta de queso con frutos rojos"},
                {"id": 15, "name": "Helado", "price": 6, "description": "3 bolas de helado a elección"}
            ]
        }
        self.orders = []

    def get_item_by_id(self, item_id):
        for category, items in self.menu_categories.items():
            for item in items:
                if item["id"] == item_id:
                    return item
        return None

    def create_order(self, customer_name, room_number, items, total_price):
        order_id = len(self.orders) + 1
        order = {
            "id": order_id,
            "customer_name": customer_name,
            "room_number": room_number,
            "items": items,
            "total_price": total_price,
            "status": "Pendiente",
            "created_at": datetime.now()
        }
        self.orders.append(order)
        return order_id

class CoflitaHotel:
    def __init__(self):
        self.rooms = [
            {
                "id": 1, 
                "name": "Habitación Estándar",
                "price": 100,
                "capacity": 2,
                "size": "25 m²",
                "bed_type": "1 Cama Doble",
                "view": "Vista a la Ciudad",
                "amenities": ["WiFi Gratis", "Aire Acondicionado", "TV", "Minibar"],
                "image": "standard.jpg",
                "description": "Habitación cómoda con todas las comodidades básicas.",
                "rating": 4.2
            },
            {
                "id": 2, 
                "name": "Suite Junior",
                "price": 150,
                "capacity": 2,
                "size": "35 m²",
                "bed_type": "1 Cama King",
                "view": "Vista Parcial al Mar",
                "amenities": ["WiFi Gratis", "Aire Acondicionado", "TV", "Minibar", "Sala de Estar", "Balcón"],
                "image": "junior.jpg",
                "description": "Suite espaciosa con sala de estar y vistas panorámicas.",
                "rating": 4.5
            },
            {
                "id": 3, 
                "name": "Suite Ejecutiva",
                "price": 200,
                "capacity": 3,
                "size": "45 m²",
                "bed_type": "1 Cama King + Sofá Cama",
                "view": "Vista al Mar",
                "amenities": ["WiFi Gratis", "Aire Acondicionado", "TV", "Minibar", "Jacuzzi", "Servicio Personalizado", "Balcón Privado"],
                "image": "executive.jpg",
                "description": "Suite de lujo con jacuzzi y servicio personalizado.",
                "rating": 4.8
            },
            {
                "id": 4, 
                "name": "Suite Familiar",
                "price": 250,
                "capacity": 4,
                "size": "60 m²",
                "bed_type": "2 Camas Dobles",
                "view": "Vista al Jardín",
                "amenities": ["WiFi Gratis", "Aire Acondicionado", "TV", "Minibar", "Cocina", "Sala de Estar", "2 Baños"],
                "image": "family.jpg",
                "description": "Amplia suite para familias con dos habitaciones separadas.",
                "rating": 4.6
            },
        ]
        self.bookings = []
        self.room_comparisons = []

    def get_room(self, room_id):
        for room in self.rooms:
            if room["id"] == room_id:
                return room
        return None

    def check_availability(self, room_id, check_in, check_out):
        for booking in self.bookings:
            if booking["room_id"] == room_id:
                if (check_in <= booking["check_out"] and check_out >= booking["check_in"]):
                    return False
        return True

    def create_booking(self, room_id, guest_name, guest_email, check_in, check_out):
        booking_id = len(self.bookings) + 1
        booking = {
            "id": booking_id,
            "room_id": room_id,
            "guest_name": guest_name,
            "guest_email": guest_email,
            "check_in": check_in,
            "check_out": check_out,
            "created_at": datetime.now()
        }
        self.bookings.append(booking)
        return booking_id

    def add_to_comparison(self, room_id):
        if room_id not in self.room_comparisons and len(self.room_comparisons) < 3:
            self.room_comparisons.append(room_id)
            return True
        return False

    def remove_from_comparison(self, room_id):
        if room_id in self.room_comparisons:
            self.room_comparisons.remove(room_id)
            return True
        return False

    def clear_comparison(self):
        self.room_comparisons = []

class CommentService:
    def __init__(self):
        self.comments = []
        self.comment_id_counter = 1
        
        # Comentarios de ejemplo
        self.add_sample_comments()
    
    def add_sample_comments(self):
        """Agrega comentarios de ejemplo para mostrar la funcionalidad"""
        sample_comments = [
            {
                "id": 1,
                "category": "comidas",
                "name": "María González",
                "rating": 5,
                "comment": "Excelente servicio de restaurante. La comida es deliciosa y el personal muy atento.",
                "date": "2024-01-15"
            },
            {
                "id": 2,
                "category": "habitaciones",
                "name": "Carlos Rodríguez",
                "rating": 4,
                "comment": "Habitaciones muy limpias y cómodas. El servicio de limpieza es impecable.",
                "date": "2024-01-14"
            },
            {
                "id": 3,
                "category": "alquiler_autos",
                "name": "Ana Martínez",
                "rating": 5,
                "comment": "Excelente servicio de alquiler de autos. Vehículos en perfecto estado y precios justos.",
                "date": "2024-01-13"
            },
            {
                "id": 4,
                "category": "hotel_general",
                "name": "Luis Pérez",
                "rating": 5,
                "comment": "Hotel espectacular en general. Ubicación perfecta, personal amable y servicios de primera.",
                "date": "2024-01-12"
            },
            {
                "id": 5,
                "category": "comidas",
                "name": "Sofía López",
                "rating": 4,
                "comment": "Buena variedad en el menú. Los desayunos son especialmente buenos.",
                "date": "2024-01-11"
            }
        ]
        
        for comment in sample_comments:
            self.comments.append(comment)
            self.comment_id_counter = max(self.comment_id_counter, comment["id"] + 1)
    
    def add_comment(self, category, name, rating, comment):
        """Agrega un nuevo comentario"""
        new_comment = {
            "id": self.comment_id_counter,
            "category": category,
            "name": name,
            "rating": rating,
            "comment": comment,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.comments.append(new_comment)
        self.comment_id_counter += 1
        return new_comment
    
    def get_comments_by_category(self, category):
        """Obtiene comentarios filtrados por categoría"""
        if category == "todos":
            return self.comments
        return [comment for comment in self.comments if comment["category"] == category]
    
    def get_all_comments(self):
        """Obtiene todos los comentarios"""
        return self.comments
    
    def get_comments_count(self):
        """Obtiene el número total de comentarios"""
        return len(self.comments)
    
    def get_average_rating_by_category(self, category):
        """Obtiene el rating promedio por categoría"""
        category_comments = self.get_comments_by_category(category)
        if not category_comments:
            return 0
        
        total_rating = sum(comment["rating"] for comment in category_comments)
        return round(total_rating / len(category_comments), 1)

def main(page: ft.Page):
    hotel = CoflitaHotel()
    email_service = EmailService()
    car_rental_service = CarRentalService()
    room_service = Servicio_a_la_habitacion()
    comment_service = CommentService()
    
    COLOR_BLUE_900 = "#1A237E"
    COLOR_BLUE_700 = "#303F9F"
    COLOR_AMBER_700 = "#FFA000"
    COLOR_WHITE = "#FFFFFF"
    COLOR_GREY_100 = "#F5F5F5"
    COLOR_GREY_300 = "#E0E0E0"
    COLOR_GREY_400 = "#BDBDBD"
    COLOR_GREY_700 = "#616161"
    COLOR_RED_400 = "#EF5350"
    COLOR_GREEN = "#4CAF50"
    
    page.title = "Hotel Coflita - Reservaciones"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.spacing = 0
    page.window_width = 1200
    page.window_height = 800
    page.scroll = ft.ScrollMode.AUTO
    
    current_view = "home"
    selected_room = None
    selected_car = None
    check_in_date = datetime.now().date()
    check_out_date = (datetime.now() + timedelta(days=1)).date()
    pickup_date = datetime.now().date()
    return_date = (datetime.now() + timedelta(days=1)).date()
    current_booking = None
    current_car_rental = None
    current_room_service_order = None
    contact_confirmation_data = None
    comment_confirmation_data = None
    room_service_cart = []



    def navigate(e, view):
        nonlocal current_view, selected_room, selected_car, check_in_date, check_out_date, current_booking, current_car_rental, current_room_service_order, contact_confirmation_data, comment_confirmation_data
        
        if view != current_view:
            if view not in ["room_details", "booking_confirmation", "car_details", "car_rental_confirmation", "room_service_cart", "room_service_confirmation"]:
                selected_room = None
                selected_car = None
                current_booking = None
                current_car_rental = None
                current_room_service_order = None
            if view != "contact_confirmation":
                contact_confirmation_data = None
            if view != "comment_confirmation":
                comment_confirmation_data = None
        
        current_view = view
        update_view()



    # Navigation bar content creation function (returns the Row content)
    def create_nav_bar_content_row():
        nav_items = [
            ft.Container(
                content=ft.Image(
                    src="/placeholder.svg?height=40&width=120&text=COFLITA",
                    height=40,
                    fit=ft.ImageFit.CONTAIN,
                ),
                padding=ft.padding.only(left=20)
            ),
            ft.Container(expand=True),
            ft.TextButton("Inicio", on_click=lambda e: navigate(e, "home"), style=ft.ButtonStyle(color=COLOR_WHITE)),
            ft.TextButton("Habitaciones", on_click=lambda e: navigate(e, "rooms"), style=ft.ButtonStyle(color=COLOR_WHITE)),
            ft.TextButton("Alquiler Autos", on_click=lambda e: navigate(e, "car_rental"), style=ft.ButtonStyle(color=COLOR_WHITE)),
            ft.TextButton("Servicio a la habitacion", on_click=lambda e: navigate(e, "room_service"), style=ft.ButtonStyle(color=COLOR_WHITE)),
            ft.TextButton("Comentarios", on_click=lambda e: navigate(e, "comments"), style=ft.ButtonStyle(color=COLOR_WHITE)),
            ft.TextButton("Contacto", on_click=lambda e: navigate(e, "contact"), style=ft.ButtonStyle(color=COLOR_WHITE)),
        ]
        
        nav_items.append(ft.Container(width=20))
        
        return ft.Row(
            nav_items,
            alignment=ft.MainAxisAlignment.CENTER,
        )

    nav_bar = ft.Container(
        content=create_nav_bar_content_row(),
        bgcolor=COLOR_BLUE_900,
        padding=15,
        width=page.window_width,
    )

    def update_nav_bar():
        nav_bar.content = create_nav_bar_content_row()
        nav_bar.update()

    footer = ft.Container(
        content=ft.Column(
            [
                ft.Divider(height=1, color=COLOR_GREY_400),
                ft.Container(height=10),
                ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text("Hotel Coflita", size=18, weight=ft.FontWeight.BOLD),
                                ft.Text("Av. Duarte Quiros 1205"),
                                ft.Text("Cordoba Capital, Argentina"),
                                ft.Text("Tel: +54 351 237-9493"),
                                ft.Text("correo: soporte.coflita@gmail.com"),
                                ft.Text("instagram: coflita2.4")
                            ],
                            spacing=5,
                        ),
                        ft.Container(expand=True),
                        ft.Column(
                            [
                                ft.Text("Servicios", size=18, weight=ft.FontWeight.BOLD),
                                ft.TextButton("Alquiler de Autos", on_click=lambda e: navigate(e, "car_rental")),
                                ft.TextButton("Servicio a la habitacion", on_click=lambda e: navigate(e, "room_service")),
                                ft.TextButton("Comparar Habitaciones", on_click=lambda e: navigate(e, "room_comparison")),
                            ],
                            spacing=5,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Container(height=10),
                ft.Text("© 2025 Hotel Coflita. Todos los derechos reservados.", size=12, color=COLOR_GREY_700),
            ],
            spacing=5,
        ),
        padding=ft.padding.all(20),
        bgcolor=COLOR_GREY_100,
        width=page.window_width,
    )

    def create_home_view():
        email_status_color = COLOR_GREEN if email_service.test_mode else COLOR_AMBER_700
        email_status_text = "🧪 Modo de prueba activado - Los emails se simulan" if email_service.test_mode else "📧 Email configurado para envío real"
        
        return ft.Column(
            [
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.PERSON, color=COLOR_WHITE),
                            ft.Text("👋 Bienvenido al Hotel Coflita", color=COLOR_WHITE, size=14),
                            ft.Container(expand=True),
                            ft.Container(width=10),
                            ft.Text(email_status_text, color=COLOR_WHITE, size=12),
                        ]
                    ),
                    bgcolor=COLOR_BLUE_700,
                    padding=10,
                ),
                
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Bienvenido a Hotel Coflita 2.4", size=40, weight=ft.FontWeight.BOLD, color=COLOR_WHITE),
                            ft.Text("Su destino perfecto para descansar y disfrutar", size=20, color=COLOR_WHITE),
                            ft.Container(height=20),
                            ft.Row([
                                ft.ElevatedButton(
                                    "Reservar Habitación",
                                    on_click=lambda e: navigate(e, "rooms"),
                                    style=ft.ButtonStyle(
                                        bgcolor=COLOR_AMBER_700,
                                        color=COLOR_WHITE,
                                        padding=ft.padding.all(15),
                                    ),
                                ),
                                ft.Container(width=20),
                                ft.ElevatedButton(
                                    "Alquilar Auto",
                                    on_click=lambda e: navigate(e, "car_rental"),
                                    style=ft.ButtonStyle(
                                        bgcolor=COLOR_BLUE_700,
                                        color=COLOR_WHITE,
                                        padding=ft.padding.all(15),
                                    ),
                                ),
                            ], alignment=ft.MainAxisAlignment.CENTER),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    width=page.window_width,
                    height=400,
                    bgcolor=COLOR_BLUE_900,
                    alignment=ft.alignment.center,
                ),
                
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Nuestros Servicios", size=30, weight=ft.FontWeight.BOLD),
                            ft.Container(height=20),
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Icon(ft.Icons.HOTEL, size=50, color=COLOR_BLUE_900),
                                                ft.Text("Habitaciones de Lujo", size=18, weight=ft.FontWeight.BOLD),
                                                ft.Text("Disfrute de nuestras cómodas y elegantes habitaciones."),
                                                ft.Container(height=10),
                                                ft.ElevatedButton(
                                                    "Ver Habitaciones",
                                                    on_click=lambda e: navigate(e, "rooms"),
                                                    style=ft.ButtonStyle(bgcolor=COLOR_BLUE_900, color=COLOR_WHITE)
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=10,
                                        ),
                                        padding=20,
                                        border_radius=10,
                                        width=280,
                                        bgcolor=COLOR_GREY_100,
                                    ),
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Icon(ft.Icons.DIRECTIONS_CAR, size=50, color=COLOR_BLUE_900),
                                                ft.Text("Alquiler de Autos", size=18, weight=ft.FontWeight.BOLD),
                                                ft.Text("Vehículos modernos y seguros para sus desplazamientos."),
                                                ft.Container(height=10),
                                                ft.ElevatedButton(
                                                    "Ver Autos",
                                                    on_click=lambda e: navigate(e, "car_rental"),
                                                    style=ft.ButtonStyle(bgcolor=COLOR_BLUE_900, color=COLOR_WHITE)
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=10,
                                        ),
                                        padding=20,
                                        border_radius=10,
                                        width=280,
                                        bgcolor=COLOR_GREY_100,
                                    ),
                                    ft.Container(
                                        content=ft.Column(
                                            [
                                                ft.Icon(ft.Icons.ROOM_SERVICE, size=50, color=COLOR_BLUE_900),
                                                ft.Text("Servicio a la habitacion", size=18, weight=ft.FontWeight.BOLD),
                                                ft.Text("Deliciosa comida entregada directamente a su habitación."),
                                                ft.Container(height=10),
                                                ft.ElevatedButton(
                                                    "Ver Menú",
                                                    on_click=lambda e: navigate(e, "room_service"),
                                                    style=ft.ButtonStyle(bgcolor=COLOR_BLUE_900, color=COLOR_WHITE)
                                                ),
                                            ],
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                            spacing=10,
                                        ),
                                        padding=20,
                                        border_radius=10,
                                        width=280,
                                        bgcolor=COLOR_GREY_100,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                spacing=20,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                    ),
                    padding=ft.padding.all(40),
                    bgcolor=COLOR_WHITE,
                ),
            ],
            spacing=0,
            scroll=ft.ScrollMode.AUTO,
        )

    def create_rooms_view():
        rooms_list = ft.Column(spacing=20, scroll=ft.ScrollMode.AUTO)
        
        # Botón de comparar habitaciones
        comparison_button = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.COMPARE_ARROWS, color=COLOR_WHITE),
                ft.Text(f"Comparar Habitaciones ({len(hotel.room_comparisons)}/3)", color=COLOR_WHITE, weight=ft.FontWeight.BOLD),
            ]),
            bgcolor=COLOR_AMBER_700 if len(hotel.room_comparisons) > 0 else COLOR_GREY_400,
            padding=15,
            border_radius=10,
            on_click=lambda e: navigate(e, "room_comparison") if len(hotel.room_comparisons) > 0 else None,
        )
        
        for room in hotel.rooms:
            is_in_comparison = room["id"] in hotel.room_comparisons
            
            room_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Container(
                                            content=ft.Image(
                                                src=f"/placeholder.svg?height=200&width=300&text={room['name']}",
                                                width=300,
                                                height=200,
                                                fit=ft.ImageFit.COVER,
                                            ),
                                            border_radius=10,
                                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                        ),
                                        ft.Container(width=20),
                                        ft.Column(
                                            [
                                                ft.Row([
                                                    ft.Text(room["name"], size=24, weight=ft.FontWeight.BOLD),
                                                    ft.Container(expand=True),
                                                    ft.Row([
                                                        ft.Icon(ft.Icons.STAR, color=COLOR_AMBER_700, size=16),
                                                        ft.Text(f"{room['rating']}", size=14, weight=ft.FontWeight.BOLD),
                                                    ]),
                                                ]),
                                                ft.Container(height=10),
                                                ft.Text(room["description"]),
                                                ft.Container(height=10),
                                                ft.Row([
                                                    ft.Column([
                                                        ft.Row([ft.Icon(ft.Icons.PERSON, color=COLOR_BLUE_900, size=16), ft.Text(f"Capacidad: {room['capacity']} personas", size=12)]),
                                                        ft.Row([ft.Icon(ft.Icons.SQUARE_FOOT, color=COLOR_BLUE_900, size=16), ft.Text(f"Tamaño: {room['size']}", size=12)]),
                                                        ft.Row([ft.Icon(ft.Icons.BED, color=COLOR_BLUE_900, size=16), ft.Text(f"{room['bed_type']}", size=12)]),
                                                    ], spacing=5),
                                                    ft.Container(width=20),
                                                    ft.Column([
                                                        ft.Row([ft.Icon(ft.Icons.LANDSCAPE, color=COLOR_BLUE_900, size=16), ft.Text(f"{room['view']}", size=12)]),
                                                        ft.Row([ft.Icon(ft.Icons.ATTACH_MONEY, color=COLOR_BLUE_900, size=16), ft.Text(f"${room['price']} por noche", weight=ft.FontWeight.BOLD, size=12)]),
                                                    ], spacing=5),
                                                ]),
                                                ft.Container(height=15),
                                                ft.Row([
                                                    ft.ElevatedButton(
                                                        "Reservar",
                                                        on_click=lambda e, r=room["id"]: show_room_details(e, r),
                                                        style=ft.ButtonStyle(bgcolor=COLOR_AMBER_700, color=COLOR_WHITE),
                                                    ),
                                                    ft.Container(width=10),
                                                    ft.ElevatedButton(
                                                        "Quitar de Comparar" if is_in_comparison else "Agregar a Comparar",
                                                        on_click=lambda e, r=room["id"]: toggle_room_comparison(e, r),
                                                        style=ft.ButtonStyle(
                                                            bgcolor=COLOR_RED_400 if is_in_comparison else COLOR_BLUE_700,
                                                             color=COLOR_WHITE
                                                        ),
                                                        disabled=not is_in_comparison and len(hotel.room_comparisons) >= 3,
                                                    ),
                                                ]),
                                            ],
                                            spacing=5,
                                            expand=True,
                                        ),
                                    ]
                                ),
                                padding=20,
                            ),
                        ]
                    ),
                    padding=0,
                ),
                elevation=3,
            )
            rooms_list.controls.append(room_card)
        
        return ft.Column([
            ft.Container(
                content=ft.Text("Nuestras Habitaciones", size=30, weight=ft.FontWeight.BOLD),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=30, bottom=20),
            ),
            ft.Container(
                content=comparison_button,
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=20),
            ),
            rooms_list,
        ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def toggle_room_comparison(e, room_id):
        if room_id in hotel.room_comparisons:
            hotel.remove_from_comparison(room_id)
            page.snack_bar = ft.SnackBar(
                content=ft.Text("Habitación removida de la comparación"),
                bgcolor=COLOR_GREEN,
            )
        else:
            if hotel.add_to_comparison(room_id):
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Habitación agregada a la comparación"),
                    bgcolor=COLOR_GREEN,
                )
            else:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Máximo 3 habitaciones para comparar"),
                    bgcolor=COLOR_RED_400,
                )
        
        page.snack_bar.open = True
        page.update()
        update_view()

    def create_room_comparison_view():
        if len(hotel.room_comparisons) == 0:
            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.COMPARE_ARROWS, size=100, color=COLOR_GREY_400),
                        ft.Container(height=20),
                        ft.Text("No hay habitaciones para comparar", size=24, weight=ft.FontWeight.BOLD),
                        ft.Container(height=10),
                        ft.Text("Agrega habitaciones desde la sección de habitaciones para compararlas aquí.", size=16, color=COLOR_GREY_700),
                        ft.Container(height=30),
                        ft.ElevatedButton(
                            "Ver Habitaciones",
                            on_click=lambda e: navigate(e, "rooms"),
                            style=ft.ButtonStyle(bgcolor=COLOR_BLUE_900, color=COLOR_WHITE, padding=ft.padding.all(15))
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.all(50),
                    alignment=ft.alignment.center,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True)

        comparison_rooms = [hotel.get_room(room_id) for room_id in hotel.room_comparisons]
        
        # Crear tabla de comparación
        comparison_table = ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.Text("Comparación de Habitaciones", size=30, weight=ft.FontWeight.BOLD),
                    ft.Container(expand=True),
                    ft.ElevatedButton(
                        "Limpiar Comparación",
                        on_click=lambda e: clear_comparison(e),
                        style=ft.ButtonStyle(bgcolor=COLOR_RED_400, color=COLOR_WHITE)
                    ),
                ]),
                padding=ft.padding.only(top=30, bottom=20),
            ),
            
            # Encabezados con imágenes
            ft.Row([
                ft.Container(width=150),  # Espacio para las etiquetas
                *[
                    ft.Container(
                        content=ft.Column([
                            ft.Image(
                                src=f"/placeholder.svg?height=150&width=200&text={room['name']}",
                                width=200,
                                height=150,
                                fit=ft.ImageFit.COVER,
                            ),
                            ft.Text(room["name"], size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                        ], spacing=10),
                        width=220,
                        padding=10,
                    ) for room in comparison_rooms
                ]
            ], alignment=ft.MainAxisAlignment.START),
            
            ft.Divider(height=2, color=COLOR_GREY_400),
            
            # Filas de comparación
            *[
                ft.Row([
                    ft.Container(
                        content=ft.Text(label, size=14, weight=ft.FontWeight.BOLD),
                        width=150,
                        padding=ft.padding.only(right=10),
                    ),
                    *[
                        ft.Container(
                            content=ft.Text(str(room[field]), size=14, text_align=ft.TextAlign.CENTER),
                            width=220,
                            padding=10,
                            bgcolor=COLOR_GREY_100 if i % 2 == 0 else COLOR_WHITE,
                        ) for room in comparison_rooms
                    ]
                ], alignment=ft.MainAxisAlignment.START)
                 for i, (label, field) in enumerate([
                    ("Precio por noche", "price"),
                    ("Capacidad", "capacity"),
                    ("Tamaño", "size"),
                    ("Tipo de cama", "bed_type"),
                    ("Vista", "view"),
                    ("Calificación", "rating"),
                ])
            ],
            
            # Amenidades
            ft.Row([
                ft.Container(
                    content=ft.Text("Amenidades", size=14, weight=ft.FontWeight.BOLD),
                    width=150,
                    padding=ft.padding.only(right=10),
                ),
                *[
                    ft.Container(
                        content=ft.Column([
                            ft.Text(amenity, size=12) for amenity in room["amenities"]
                        ], spacing=2),
                        width=220,
                        padding=10,
                        bgcolor=COLOR_GREY_100,
                    ) for room in comparison_rooms
                ]
            ], alignment=ft.MainAxisAlignment.START),
            
            ft.Container(height=30),
            
            # Botones de acción
            ft.Row([
                ft.Container(width=150),
                *[
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Reservar Esta",
                            on_click=lambda e, r=room["id"]: show_room_details(e, r),
                            style=ft.ButtonStyle(bgcolor=COLOR_AMBER_700, color=COLOR_WHITE, padding=ft.padding.all(15)),
                        ),
                        width=220,
                        alignment=ft.alignment.center,
                    ) for room in comparison_rooms
                ]
            ], alignment=ft.MainAxisAlignment.START),
            
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
        
        return comparison_table

    def clear_comparison(e):
        hotel.clear_comparison()
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Comparación limpiada"),
            bgcolor=COLOR_GREEN,
        )
        page.snack_bar.open = True
        page.update()
        navigate(e, "rooms")

    def show_room_details(e, room_id):
        nonlocal current_view, selected_room
        selected_room = hotel.get_room(room_id)
        current_view = "room_details"
        update_view()

    def create_room_details_view():
        nonlocal check_in_date, check_out_date
        
        if not selected_room:
            return ft.Text("Habitación no encontrada")
        
        guest_name = ft.TextField(label="Nombre completo", border=ft.InputBorder.OUTLINE)
        guest_email = ft.TextField(label="Correo electrónico", border=ft.InputBorder.OUTLINE)
        
        check_in_display = ft.Text(f"Fecha de entrada: {check_in_date.strftime('%d/%m/%Y')}")
        check_out_display = ft.Text(f"Fecha de salida: {check_out_date.strftime('%d/%m/%Y')}")
        
        def update_check_in_date(e):
            nonlocal check_in_date, check_out_date
            if e.control.value:
                check_in_date = e.control.value.date()
                if check_out_date <= check_in_date:
                    check_out_date = check_in_date + timedelta(days=1)
                    check_out_display.value = f"Fecha de salida: {check_out_date.strftime('%d/%m/%Y')}"
                check_in_display.value = f"Fecha de entrada: {check_in_date.strftime('%d/%m/%Y')}"
                page.update()

        def update_check_out_date(e):
            nonlocal check_out_date
            if e.control.value:
                selected_date = e.control.value.date()
                if selected_date > check_in_date:
                    check_out_date = selected_date
                    check_out_display.value = f"Fecha de salida: {check_out_date.strftime('%d/%m/%Y')}"
                    page.update()
                else:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("La fecha de salida debe ser posterior a la fecha de entrada"),
                        bgcolor=COLOR_RED_400,
                    )
                    page.snack_bar.open = True
                    page.update()
        
        check_in_picker = ft.DatePicker(
            first_date=datetime.now(),
            last_date=datetime.now() + timedelta(days=365),
            on_change=update_check_in_date,
        )
        check_out_picker = ft.DatePicker(
            first_date=datetime.now() + timedelta(days=1),
            last_date=datetime.now() + timedelta(days=366),
            on_change=update_check_out_date,
        )
        page.overlay.extend([check_in_picker, check_out_picker])

        def open_check_in_picker(e):
            check_in_picker.open = True
            page.update()

        def open_check_out_picker(e):
            check_out_picker.open = True
            page.update()
        
        def submit_booking(e):
            nonlocal current_booking
            try:
                if not guest_name.value or not guest_name.value.strip():
                    page.snack_bar = ft.SnackBar(content=ft.Text("Por favor ingrese su nombre completo"), bgcolor=COLOR_RED_400)
                    page.snack_bar.open = True
                    page.update()
                    return
                
                if not guest_email.value or not guest_email.value.strip():
                    page.snack_bar = ft.SnackBar(content=ft.Text("Por favor ingrese su correo electrónico"), bgcolor=COLOR_RED_400)
                    page.snack_bar.open = True
                    page.update()
                    return
                
                if "@" not in guest_email.value or "." not in guest_email.value:
                    page.snack_bar = ft.SnackBar(content=ft.Text("Por favor ingrese un correo electrónico válido"), bgcolor=COLOR_RED_400)
                    page.snack_bar.open = True
                    page.update()
                    return
                
                if check_in_date >= check_out_date:
                    page.snack_bar = ft.SnackBar(content=ft.Text("La fecha de salida debe ser posterior a la fecha de entrada"), bgcolor=COLOR_RED_400)
                    page.snack_bar.open = True
                    page.update()
                    return
                
                if check_in_date < datetime.now().date():
                    page.snack_bar = ft.SnackBar(content=ft.Text("La fecha de entrada no puede ser en el pasado"), bgcolor=COLOR_RED_400)
                    page.snack_bar.open = True
                    page.update()
                    return
                
                if not hotel.check_availability(selected_room["id"], check_in_date, check_out_date):
                    page.snack_bar = ft.SnackBar(content=ft.Text("Lo sentimos, la habitación no está disponible en esas fechas"), bgcolor=COLOR_RED_400)
                    page.snack_bar.open = True
                    page.update()
                    return
                
                booking_id = hotel.create_booking(
                    selected_room["id"],
                    guest_name.value.strip(),
                    guest_email.value.strip(),
                    check_in_date,
                    check_out_date
                )
                
                nights = (check_out_date - check_in_date).days
                total_price = selected_room['price'] * nights
                current_booking = {
                    'id': booking_id,
                    'guest_name': guest_name.value.strip(),
                    'guest_email': guest_email.value.strip(),
                    'nights': nights,
                    'total_price': total_price
                }
                
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("🎉 Reserva creada! Enviando confirmación por email..."),
                    bgcolor=COLOR_GREEN,
                )
                page.snack_bar.open = True
                page.update()
                
                # Enviar email de confirmación
                success, message = email_service.send_booking_confirmation(
                    guest_email.value.strip(),
                    guest_name.value.strip(),
                    selected_room["name"],
                    check_in_date,
                    check_out_date,
                    nights,
                    total_price,
                    booking_id
                )
                
                if success:
                    print(f"✅ Email de confirmación enviado a {guest_email.value.strip()}")
                else:
                    print(f"❌ Error al enviar email: {message}")
                
                nonlocal current_view
                current_view = "booking_confirmation"
                update_view()
                
            except Exception as ex:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Error al procesar la reserva: {str(ex)}"), bgcolor=COLOR_RED_400)
                page.snack_bar.open = True
                page.update()
                print(f"Error en submit_booking: {ex}")
        
        return ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: navigate(e, "rooms")),
                    ft.Text(selected_room["name"], size=30, weight=ft.FontWeight.BOLD),
                ]),
                padding=ft.padding.only(top=30, bottom=20),
            ),
            ft.Row([
                ft.Container(
                    content=ft.Image(
                        src=f"/placeholder.svg?height=300&width=500&text={selected_room['name']}",
                        width=500, height=300, fit=ft.ImageFit.COVER,
                    ),
                    border_radius=10, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                ),
                ft.Container(width=30),
                ft.Column([
                    ft.Text("Detalles de la habitación", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    ft.Text(selected_room["description"]),
                    ft.Container(height=10),
                    ft.Row([ft.Icon(ft.Icons.PERSON, color=COLOR_BLUE_900), ft.Text(f"Capacidad: {selected_room['capacity']} personas")]),
                    ft.Container(height=5),
                    ft.Row([ft.Icon(ft.Icons.SQUARE_FOOT, color=COLOR_BLUE_900), ft.Text(f"Tamaño: {selected_room['size']}")]),
                    ft.Container(height=5),
                    ft.Row([ft.Icon(ft.Icons.BED, color=COLOR_BLUE_900), ft.Text(f"{selected_room['bed_type']}")]),
                    ft.Container(height=5),
                    ft.Row([ft.Icon(ft.Icons.LANDSCAPE, color=COLOR_BLUE_900), ft.Text(f"{selected_room['view']}")]),
                    ft.Container(height=5),
                    ft.Row([ft.Icon(ft.Icons.ATTACH_MONEY, color=COLOR_BLUE_900), ft.Text(f"Precio: ${selected_room['price']} por noche", weight=ft.FontWeight.BOLD)]),
                    ft.Container(height=10),
                    ft.Text("Amenidades:", weight=ft.FontWeight.BOLD),
                    ft.Column([
                        ft.Text(f"• {amenity}") for amenity in selected_room["amenities"]
                    ], spacing=2),
                ], spacing=5, expand=True),
            ]),
            ft.Container(height=30),
            ft.Text("Formulario de Reserva", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        guest_name,
                        ft.Container(height=10),
                        guest_email,
                        ft.Container(height=20),
                        ft.Text("Seleccione las fechas de su estancia:", size=16),
                        ft.Container(height=10),
                        ft.Row([
                            ft.Column([
                                check_in_display,
                                ft.ElevatedButton("Seleccionar fecha de entrada", on_click=open_check_in_picker, style=ft.ButtonStyle(bgcolor=COLOR_BLUE_700, color=COLOR_WHITE)),
                            ], spacing=10),
                            ft.Container(width=30),
                            ft.Column([
                                check_out_display,
                                ft.ElevatedButton("Seleccionar fecha de salida", on_click=open_check_out_picker, style=ft.ButtonStyle(bgcolor=COLOR_BLUE_700, color=COLOR_WHITE)),
                            ], spacing=10),
                        ]),
                        ft.Container(height=30),
                        ft.ElevatedButton("Confirmar Reserva", on_click=submit_booking, style=ft.ButtonStyle(bgcolor=COLOR_AMBER_700, color=COLOR_WHITE, padding=ft.padding.all(15))),
                    ], spacing=10),
                    padding=30,
                ),
                elevation=3,
            ),
        ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def create_booking_confirmation_view():
        if not selected_room or not current_booking:
            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ERROR, size=100, color=COLOR_RED_400),
                        ft.Container(height=20),
                        ft.Text("Error en la Reserva", size=30, weight=ft.FontWeight.BOLD),
                        ft.Container(height=10),
                        ft.Text("No se pudo procesar la reserva. Por favor intente nuevamente.", size=18),
                        ft.Container(height=30),
                        ft.ElevatedButton("Volver al inicio", on_click=lambda e: navigate(e, "home"), style=ft.ButtonStyle(bgcolor=COLOR_BLUE_900, color=COLOR_WHITE, padding=ft.padding.all(15))),
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.all(50), alignment=ft.alignment.center,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True)
        
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=100, color=COLOR_GREEN),
                    ft.Container(height=20),
                    ft.Text("¡Reserva Confirmada!", size=30, weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    ft.Text("Su reserva ha sido procesada con éxito.", size=18),
                    ft.Container(height=30),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text("Detalles de la Reserva", size=20, weight=ft.FontWeight.BOLD),
                                ft.Container(height=10),
                                ft.Text(f"Número de Reserva: #{current_booking['id']:04d}", size=16, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                                ft.Text(f"Número de habitacion: #{current_booking['id']:04d}", size=16, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),   
                                ft.Text(f"Huésped: {current_booking['guest_name']}", size=16),
                                ft.Text(f"Email: {current_booking['guest_email']}", size=16),
                                ft.Text(f"Habitación: {selected_room['name']}", size=16),
                                ft.Text(f"Fecha de entrada: {check_in_date.strftime('%d/%m/%Y')}", size=16),
                                ft.Text(f"Fecha de salida: {check_out_date.strftime('%d/%m/%Y')}", size=16),
                                ft.Text(f"Número de noches: {current_booking['nights']}", size=16),
                                ft.Text(f"Precio por noche: ${selected_room['price']}", size=16),
                                ft.Container(height=5),
                                ft.Divider(height=1, color=COLOR_GREY_400),
                                ft.Container(height=5),
                                ft.Text(f"Precio total: ${current_booking['total_price']}", size=18, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                            ], spacing=10),
                            padding=30,
                        ),
                        elevation=3,
                    ),
                    ft.Container(height=30),
                    ft.Container(
                        content=ft.Column([
                            ft.Row([ft.Icon(ft.Icons.EMAIL, color=COLOR_BLUE_900), ft.Text("Confirmación por Email", size=16, weight=ft.FontWeight.BOLD)]),
                            ft.Text(f"Email enviado a: {current_booking['guest_email']}", size=14),
                            ft.Text("Revisa tu bandeja de entrada para ver los detalles completos.", size=12, color=COLOR_GREY_700),
                        ], spacing=5),
                        padding=15, bgcolor=COLOR_GREY_100, border_radius=10,
                    ),
                    ft.Container(height=20),
                    ft.Row([
                        ft.ElevatedButton("Volver al inicio", on_click=lambda e: navigate(e, "home"), style=ft.ButtonStyle(bgcolor=COLOR_BLUE_900, color=COLOR_WHITE, padding=ft.padding.all(15))),
                        ft.Container(width=20),
                        ft.ElevatedButton("Ver habitaciones", on_click=lambda e: navigate(e, "rooms"), style=ft.ButtonStyle(bgcolor=COLOR_AMBER_700, color=COLOR_WHITE, padding=ft.padding.all(15))),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(50), alignment=ft.alignment.center,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True)

    # CAR RENTAL VIEWS
    def create_car_rental_view():
        cars_list = ft.Column(spacing=20, scroll=ft.ScrollMode.AUTO)
        
        for car in car_rental_service.cars:
            car_card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Container(
                                            content=ft.Image(
                                                src=f"/placeholder.svg?height=200&width=300&text={car['name']}",
                                                width=300,
                                                height=200,
                                                fit=ft.ImageFit.COVER,
                                            ),
                                            border_radius=10,
                                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                        ),
                                        ft.Container(width=20),
                                        ft.Column(
                                            [
                                                ft.Text(car["name"], size=24, weight=ft.FontWeight.BOLD),
                                                ft.Container(height=5),
                                                ft.Text(f"Categoría: {car['category']}", size=16, color=COLOR_BLUE_900, weight=ft.FontWeight.BOLD),
                                                ft.Container(height=10),
                                                ft.Row([ft.Icon(ft.Icons.PERSON, color=COLOR_BLUE_900), ft.Text(f"Capacidad: {car['capacity']} personas")]),
                                                ft.Container(height=5),
                                                ft.Row([ft.Icon(ft.Icons.SETTINGS, color=COLOR_BLUE_900), ft.Text(f"Transmisión: {car['transmission']}")]),
                                                ft.Container(height=5),
                                                ft.Row([ft.Icon(ft.Icons.LOCAL_GAS_STATION, color=COLOR_BLUE_900), ft.Text(f"Combustible: {car['fuel']}")]),
                                                ft.Container(height=5),
                                                ft.Row([ft.Icon(ft.Icons.ATTACH_MONEY, color=COLOR_BLUE_900), ft.Text(f"Precio: ${car['price_per_day']} por día", weight=ft.FontWeight.BOLD)]),
                                                ft.Container(height=10),
                                                ft.Text("Características:", weight=ft.FontWeight.BOLD),
                                                ft.Column([
                                                    ft.Text(f"• {feature}") for feature in car["features"]
                                                ], spacing=2),
                                                ft.Container(height=15),
                                                ft.ElevatedButton(
                                                    "Alquilar Ahora",
                                                    on_click=lambda e, c=car["id"]: show_car_details(e, c),
                                                    style=ft.ButtonStyle(bgcolor=COLOR_AMBER_700, color=COLOR_WHITE),
                                                ),
                                            ],
                                            spacing=5,
                                            expand=True,
                                        ),
                                    ]
                                ),
                                padding=20,
                            ),
                        ]
                    ),
                    padding=0,
                ),
                elevation=3,
            )
            cars_list.controls.append(car_card)
        
        return ft.Column([
            ft.Container(
                content=ft.Text("Alquiler de Autos", size=30, weight=ft.FontWeight.BOLD),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=30, bottom=20),
            ),
            ft.Container(
                content=ft.Text("Vehículos modernos y seguros para sus desplazamientos", size=16, color=COLOR_GREY_700),
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=30),
            ),
            cars_list,
        ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def show_car_details(e, car_id):
        nonlocal current_view, selected_car
        selected_car = car_rental_service.get_car(car_id)
        current_view = "car_details"
        update_view()

    def create_car_details_view():
        nonlocal pickup_date, return_date
        
        if not selected_car:
            return ft.Text("Vehículo no encontrado")
        
        customer_name = ft.TextField(label="Nombre completo", border=ft.InputBorder.OUTLINE)
        customer_email = ft.TextField(label="Correo electrónico", border=ft.InputBorder.OUTLINE)
        
        pickup_display = ft.Text(f"Fecha de recogida: {pickup_date.strftime('%d/%m/%Y')}")
        return_display = ft.Text(f"Fecha de devolución: {return_date.strftime('%d/%m/%Y')}")
        
        def update_pickup_date(e):
            nonlocal pickup_date, return_date
            if e.control.value:
                pickup_date = e.control.value.date()
                if return_date <= pickup_date:
                    return_date = pickup_date + timedelta(days=1)
                    return_display.value = f"Fecha de devolución: {return_date.strftime('%d/%m/%Y')}"
                pickup_display.value = f"Fecha de recogida: {pickup_date.strftime('%d/%m/%Y')}"
                page.update()

        def update_return_date(e):
            nonlocal return_date
            if e.control.value:
                selected_date = e.control.value.date()
                if selected_date > pickup_date:
                    return_date = selected_date
                    return_display.value = f"Fecha de devolución: {return_date.strftime('%d/%m/%Y')}"
                    page.update()
                else:
                    page.snack_bar = ft.SnackBar(
                        content=ft.Text("La fecha de devolución debe ser posterior a la fecha de recogida"),
                        bgcolor=COLOR_RED_400,
                    )
                    page.snack_bar.open = True
                    page.update()
        
        pickup_picker = ft.DatePicker(
            first_date=datetime.now(),
            last_date=datetime.now() + timedelta(days=365),
            on_change=update_pickup_date,
        )
        return_picker = ft.DatePicker(
            first_date=datetime.now() + timedelta(days=1),
            last_date=datetime.now() + timedelta(days=366),
            on_change=update_return_date,
        )
        page.overlay.extend([pickup_picker, return_picker])

        def open_pickup_picker(e):
            pickup_picker.open = True
            page.update()

        def open_return_picker(e):
            return_picker.open = True
            page.update()
        
        def submit_car_rental(e):
            nonlocal current_car_rental
            try:
                if not customer_name.value or not customer_name.value.strip():
                    page.snack_bar = ft.SnackBar(content=ft.Text("Por favor ingrese su nombre completo"), bgcolor=COLOR_RED_400)
                    page.snack_bar.open = True
                    page.update()
                    return
                
                if not customer_email.value or not customer_email.value.strip():
                    page.snack_bar = ft.SnackBar(content=ft.Text("Por favor ingrese su correo electrónico"), bgcolor=COLOR_RED_400)
                    page.snack_bar.open = True
                    page.update()
                    return
                
                if "@" not in customer_email.value or "." not in customer_email.value:
                    page.snack_bar = ft.SnackBar(content=ft.Text("Por favor ingrese un correo electrónico válido"), bgcolor=COLOR_RED_400)
                    page.snack_bar.open = True
                    page.update()
                    return
                
                if pickup_date >= return_date:
                    page.snack_bar = ft.SnackBar(content=ft.Text("La fecha de devolución debe ser posterior a la fecha de recogida"), bgcolor=COLOR_RED_400)
                    page.snack_bar.open = True
                    page.update()
                    return
                
                if pickup_date < datetime.now().date():
                    page.snack_bar = ft.SnackBar(content=ft.Text("La fecha de recogida no puede ser en el pasado"), bgcolor=COLOR_RED_400)
                    page.snack_bar.open = True
                    page.update()
                    return
                
                rental_id = car_rental_service.create_rental(
                    selected_car["id"],
                    customer_name.value.strip(),
                    customer_email.value.strip(),
                    pickup_date,
                    return_date
                )
                
                days = (return_date - pickup_date).days
                total_price = selected_car['price_per_day'] * days
                current_car_rental = {
                    'id': rental_id,
                    'customer_name': customer_name.value.strip(),
                    'customer_email': customer_email.value.strip(),
                    'days': days,
                    'total_price': total_price
                }
                
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("🎉 Alquiler confirmado!"),
                    bgcolor=COLOR_GREEN,
                )
                page.snack_bar.open = True
                page.update()
                
                print("🚗 ALQUILER DE AUTO CONFIRMADO:")
                print(f"👤 Cliente: {customer_name.value.strip()}")
                print(f"📧 Email: {customer_email.value.strip()}")
                print(f"🚗 Vehículo: {selected_car['name']}")
                print(f"📅 Recogida: {pickup_date.strftime('%d/%m/%Y')}")
                print(f"📅 Devolución: {return_date.strftime('%d/%m/%Y')}")
                print(f"📊 Días: {days}")
                print(f"💰 Total: ${total_price}")
                print(f"🔢 Alquiler #: {rental_id:04d}")
                print("=" * 50)
                
                nonlocal current_view
                current_view = "car_rental_confirmation"
                update_view()
                
            except Exception as ex:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Error al procesar el alquiler: {str(ex)}"), bgcolor=COLOR_RED_400)
                page.snack_bar.open = True
                page.update()
                print(f"Error en submit_car_rental: {ex}")
        
        return ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: navigate(e, "car_rental")),
                    ft.Text(selected_car["name"], size=30, weight=ft.FontWeight.BOLD),
                ]),
                padding=ft.padding.only(top=30, bottom=20),
            ),
            ft.Row([
                ft.Container(
                    content=ft.Image(
                        src=f"/placeholder.svg?height=300&width=500&text={selected_car['name']}",
                        width=500, height=300, fit=ft.ImageFit.COVER,
                    ),
                    border_radius=10, clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                ),
                ft.Container(width=30),
                ft.Column([
                    ft.Text("Detalles del Vehículo", size=20, weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    ft.Text(f"Categoría: {selected_car['category']}", size=16, color=COLOR_BLUE_900, weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    ft.Row([ft.Icon(ft.Icons.PERSON, color=COLOR_BLUE_900), ft.Text(f"Capacidad: {selected_car['capacity']} personas")]),
                    ft.Container(height=5),
                    ft.Row([ft.Icon(ft.Icons.SETTINGS, color=COLOR_BLUE_900), ft.Text(f"Transmisión: {selected_car['transmission']}")]),
                    ft.Container(height=5),
                    ft.Row([ft.Icon(ft.Icons.LOCAL_GAS_STATION, color=COLOR_BLUE_900), ft.Text(f"Combustible: {selected_car['fuel']}")]),
                    ft.Container(height=5),
                    ft.Row([ft.Icon(ft.Icons.ATTACH_MONEY, color=COLOR_BLUE_900), ft.Text(f"Precio: ${selected_car['price_per_day']} por día", weight=ft.FontWeight.BOLD)]),
                    ft.Container(height=10),
                    ft.Text("Características:", weight=ft.FontWeight.BOLD),
                    ft.Column([
                        ft.Text(f"• {feature}") for feature in selected_car["features"]
                    ], spacing=2),
                ], spacing=5, expand=True),
            ]),
            ft.Container(height=30),
            ft.Text("Formulario de Alquiler", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        customer_name,
                        ft.Container(height=10),
                        customer_email,
                        ft.Container(height=20),
                        ft.Text("Seleccione las fechas de alquiler:", size=16),
                        ft.Container(height=10),
                        ft.Row([
                            ft.Column([
                                pickup_display,
                                ft.ElevatedButton("Seleccionar fecha de recogida", on_click=open_pickup_picker, style=ft.ButtonStyle(bgcolor=COLOR_BLUE_700, color=COLOR_WHITE)),
                            ], spacing=10),
                            ft.Container(width=30),
                            ft.Column([
                                return_display,
                                ft.ElevatedButton("Seleccionar fecha de devolución", on_click=open_return_picker, style=ft.ButtonStyle(bgcolor=COLOR_BLUE_700, color=COLOR_WHITE)),
                            ], spacing=10),
                        ]),
                        ft.Container(height=30),
                        ft.ElevatedButton("Confirmar Alquiler", on_click=submit_car_rental, style=ft.ButtonStyle(bgcolor=COLOR_AMBER_700, color=COLOR_WHITE, padding=ft.padding.all(15))),
                    ], spacing=10),
                    padding=30,
                ),
                elevation=3,
            ),
        ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def create_car_rental_confirmation_view():
        if not selected_car or not current_car_rental:
            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ERROR, size=100, color=COLOR_RED_400),
                        ft.Container(height=20),
                        ft.Text("Error en el Alquiler", size=30, weight=ft.FontWeight.BOLD),
                        ft.Container(height=10),
                        ft.Text("No se pudo procesar el alquiler. Por favor intente nuevamente.", size=18),
                        ft.Container(height=30),
                        ft.ElevatedButton("Volver al inicio", on_click=lambda e: navigate(e, "home"), style=ft.ButtonStyle(bgcolor=COLOR_BLUE_900, color=COLOR_WHITE, padding=ft.padding.all(15))),
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.all(50), alignment=ft.alignment.center,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True)
        
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=100, color=COLOR_GREEN),
                    ft.Container(height=20),
                    ft.Text("¡Alquiler Confirmado!", size=30, weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    ft.Text("Su alquiler de vehículo ha sido procesado con éxito.", size=18),
                    ft.Container(height=30),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text("Detalles del Alquiler", size=20, weight=ft.FontWeight.BOLD),
                                ft.Container(height=10),
                                ft.Text(f"Número de Alquiler: #{current_car_rental['id']:04d}", size=16, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                                ft.Text(f"Cliente: {current_car_rental['customer_name']}", size=16),
                                ft.Text(f"Email: {current_car_rental['customer_email']}", size=16),
                                ft.Text(f"Vehículo: {selected_car['name']}", size=16),
                                ft.Text(f"Categoría: {selected_car['category']}", size=16),
                                ft.Text(f"Fecha de retiro: {pickup_date.strftime('%d/%m/%Y')}", size=16),
                                ft.Text(f"Fecha de devolución: {return_date.strftime('%d/%m/%Y')}", size=16),
                                ft.Text(f"Número de días: {current_car_rental['days']}", size=16),
                                ft.Text(f"Precio por día: ${selected_car['price_per_day']}", size=16),
                                ft.Container(height=5),
                                ft.Divider(height=1, color=COLOR_GREY_400),
                                ft.Container(height=5),
                                ft.Text(f"Precio total: ${current_car_rental['total_price']}", size=18, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                            ], spacing=10),
                            padding=30,
                        ),
                        elevation=3,
                    ),
                    ft.Container(height=30),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("📍 Información de Retiro", size=16, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                            ft.Text("Ubicación: Hotel Coflita - Lobby Principal", size=14),
                            ft.Text("Horario: 8:00 AM - 8:00 PM", size=14),
                            ft.Text("Documentos necesarios: Licencia de conducir válida, DNI y tarjeta de credito", size=12, color=COLOR_GREY_700),
                        ], spacing=5),
                        padding=15, bgcolor=COLOR_GREY_100, border_radius=10,
                    ),
                    ft.Container(height=20),
                    ft.Row([
                        ft.ElevatedButton("Volver al inicio", on_click=lambda e: navigate(e, "home"), style=ft.ButtonStyle(bgcolor=COLOR_BLUE_900, color=COLOR_WHITE, padding=ft.padding.all(15))),
                        ft.Container(width=20),
                        ft.ElevatedButton("Ver más autos", on_click=lambda e: navigate(e, "car_rental"), style=ft.ButtonStyle(bgcolor=COLOR_AMBER_700, color=COLOR_WHITE, padding=ft.padding.all(15))),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(50), alignment=ft.alignment.center,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True)

    # ROOM SERVICE VIEWS
    def create_room_service_view():
        menu_sections = ft.Column(spacing=20, scroll=ft.ScrollMode.AUTO)
        
        # Cart summary
        cart_total = sum(item['price'] * item['quantity'] for item in room_service_cart)
        cart_summary = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.SHOPPING_CART, color=COLOR_WHITE),
                ft.Text(f"Carrito ({len(room_service_cart)} items) - Total: ${cart_total}", color=COLOR_WHITE, weight=ft.FontWeight.BOLD),
                ft.Container(expand=True),
                ft.ElevatedButton(
                    "Ver Carrito",
                    on_click=lambda e: navigate(e, "room_service_cart"),
                    style=ft.ButtonStyle(bgcolor=COLOR_WHITE, color=COLOR_BLUE_900),
                    disabled=len(room_service_cart) == 0,
                ),
            ]),
            bgcolor=COLOR_BLUE_900 if len(room_service_cart) > 0 else COLOR_GREY_400,
            padding=15,
            border_radius=10,
        )
        
        for category, items in room_service.menu_categories.items():
            category_section = ft.Container(
                content=ft.Column([
                    ft.Text(category, size=24, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                    ft.Container(height=15),
                    ft.Column([
                        ft.Card(
                            content=ft.Container(
                                content=ft.Row([
                                    ft.Container(
                                        content=ft.Image(
                                            src=f"/placeholder.svg?height=100&width=150&text={item['name']}",
                                            width=150,
                                            height=100,
                                            fit=ft.ImageFit.COVER,
                                        ),
                                        border_radius=10,
                                        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                                    ),
                                    ft.Container(width=15),
                                    ft.Column([
                                        ft.Text(item["name"], size=18, weight=ft.FontWeight.BOLD),
                                        ft.Container(height=5),
                                        ft.Text(item["description"], size=14, color=COLOR_GREY_700),
                                        ft.Container(height=10),
                                        ft.Row([
                                            ft.Text(f"${item['price']}", size=16, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                                            ft.Container(expand=True),
                                            ft.ElevatedButton(
                                                "Agregar al Carrito",
                                                on_click=lambda e, item_id=item["id"]: add_to_cart(e, item_id),
                                                style=ft.ButtonStyle(bgcolor=COLOR_AMBER_700, color=COLOR_WHITE),
                                            ),
                                        ]),
                                    ], expand=True),
                                ]),
                                padding=15,
                            ),
                            elevation=2,
                        ) for item in items
                    ], spacing=10),
                ]),
                padding=ft.padding.only(bottom=30),
            )
            menu_sections.controls.append(category_section)
        
        return ft.Column([
            ft.Container(
                content=ft.Text("Servicio a la habitacion", size=30, weight=ft.FontWeight.BOLD),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=30, bottom=20),
            ),
            ft.Container(
                content=ft.Text("Deliciosa comida entregada directamente a su habitación", size=16, color=COLOR_GREY_700),
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=20),
            ),
            cart_summary,
            ft.Container(height=20),
            menu_sections,
        ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def add_to_cart(e, item_id):
        nonlocal room_service_cart
        item = room_service.get_item_by_id(item_id)
        if item:
            # Check if item already in cart
            existing_item = next((cart_item for cart_item in room_service_cart if cart_item['id'] == item_id), None)
            if existing_item:
                existing_item['quantity'] += 1
            else:
                cart_item = item.copy()
                cart_item['quantity'] = 1
                room_service_cart.append(cart_item)
            
            page.snack_bar = ft.SnackBar(
                content=ft.Text(f"✅ {item['name']} agregado al carrito"),
                bgcolor=COLOR_GREEN,
            )
            page.snack_bar.open = True
            page.update()
            update_view()

    def create_room_service_cart_view():
        if len(room_service_cart) == 0:
            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.SHOPPING_CART_OUTLINED, size=100, color=COLOR_GREY_400),
                        ft.Container(height=20),
                        ft.Text("Carrito Vacío", size=24, weight=ft.FontWeight.BOLD),
                        ft.Container(height=10),
                        ft.Text("Agrega algunos elementos del menú para continuar.", size=16, color=COLOR_GREY_700),
                        ft.Container(height=30),
                        ft.ElevatedButton(
                            "Ver Menú",
                            on_click=lambda e: navigate(e, "room_service"),
                            style=ft.ButtonStyle(bgcolor=COLOR_BLUE_900, color=COLOR_WHITE, padding=ft.padding.all(15))
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.all(50),
                    alignment=ft.alignment.center,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True)

        cart_items = ft.Column(spacing=15, scroll=ft.ScrollMode.AUTO)
        total_price = 0
        
        for item in room_service_cart:
            item_total = item['price'] * item['quantity']
            total_price += item_total
            
            cart_item = ft.Card(
                content=ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Image(
                                src=f"/placeholder.svg?height=80&width=120&text={item['name']}",
                                width=120,
                                height=80,
                                fit=ft.ImageFit.COVER,
                            ),
                            border_radius=10,
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                        ),
                        ft.Container(width=15),
                        ft.Column([
                            ft.Text(item["name"], size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(item["description"], size=12, color=COLOR_GREY_700),
                            ft.Text(f"${item['price']} c/u", size=14, color=COLOR_BLUE_900),
                        ], expand=True),
                        ft.Column([
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.REMOVE,
                                    on_click=lambda e, item_id=item["id"]: update_cart_quantity(e, item_id, -1),
                                    style=ft.ButtonStyle(bgcolor=COLOR_GREY_300),
                                ),
                                ft.Text(str(item['quantity']), size=16, weight=ft.FontWeight.BOLD),
                                ft.IconButton(
                                    icon=ft.Icons.ADD,
                                    on_click=lambda e, item_id=item["id"]: update_cart_quantity(e, item_id, 1),
                                    style=ft.ButtonStyle(bgcolor=COLOR_GREEN),
                                ),
                            ], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Text(f"${item_total}", size=14, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                            ft.TextButton(
                                "Eliminar",
                                on_click=lambda e, item_id=item["id"]: remove_from_cart(e, item_id),
                                style=ft.ButtonStyle(color=COLOR_RED_400),
                            ),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    ]),
                    padding=15,
                ),
                elevation=2,
            )
            cart_items.controls.append(cart_item)
        
        # Order form
        customer_name = ft.TextField(label="Nombre completo", border=ft.InputBorder.OUTLINE, width=300)
        room_number = ft.TextField(label="Número de habitación", border=ft.InputBorder.OUTLINE, width=300)
        
        def submit_room_service_order(e):
            nonlocal current_room_service_order
            try:
                if not customer_name.value or not customer_name.value.strip():
                    page.snack_bar = ft.SnackBar(content=ft.Text("Por favor ingrese su nombre completo"), bgcolor=COLOR_RED_400)
                    page.snack_bar.open = True
                    page.update()
                    return
                
                if not room_number.value or not room_number.value.strip():
                    page.snack_bar = ft.SnackBar(content=ft.Text("Por favor ingrese el número de habitación"), bgcolor=COLOR_RED_400)
                    page.snack_bar.open = True
                    page.update()
                    return
                
                order_id = room_service.create_order(
                    customer_name.value.strip(),
                    room_number.value.strip(),
                    room_service_cart.copy(),
                    total_price
                )
                
                current_room_service_order = {
                    'id': order_id,
                    'customer_name': customer_name.value.strip(),
                    'room_number': room_number.value.strip(),
                    'items': room_service_cart.copy(),
                    'total_price': total_price
                }
                
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("🎉 Pedido confirmado!"),
                    bgcolor=COLOR_GREEN,
                )
                page.snack_bar.open = True
                page.update()
                
                print("🍽️ PEDIDO DE SERVICIO A LA HABITACION CONFIRMADO:")
                print(f"👤 Cliente: {customer_name.value.strip()}")
                print(f"🏨 Habitación: {room_number.value.strip()}")
                print(f"📋 Items:")
                for item in room_service_cart:
                    print(f"   • {item['name']} x{item['quantity']} - ${item['price'] * item['quantity']}")
                print(f"💰 Total: ${total_price}")
                print(f"🔢 Pedido #: {order_id:04d}")
                print("=" * 50)
                
                # Clear cart
                room_service_cart.clear()
                
                nonlocal current_view
                current_view = "room_service_confirmation"
                update_view()
                
            except Exception as ex:
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Error al procesar el pedido: {str(ex)}"), bgcolor=COLOR_RED_400)
                page.snack_bar.open = True
                page.update()
                print(f"Error en submit_room_service_order: {ex}")
        
        return ft.Column([
            ft.Container(
                content=ft.Row([
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, on_click=lambda e: navigate(e, "room_service")),
                    ft.Text("Carrito de servicio a la habitacion", size=30, weight=ft.FontWeight.BOLD),
                ]),
                padding=ft.padding.only(top=30, bottom=20),
            ),
            cart_items,
            ft.Container(height=20),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Resumen del Pedido", size=20, weight=ft.FontWeight.BOLD),
                        ft.Container(height=15),
                        ft.Row([
                            ft.Text("Total:", size=18, weight=ft.FontWeight.BOLD),
                            ft.Container(expand=True),
                            ft.Text(f"${total_price}", size=18, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                        ]),
                        ft.Container(height=20),
                        ft.Text("Información de Entrega", size=16, weight=ft.FontWeight.BOLD),
                        ft.Container(height=10),
                        customer_name,
                        ft.Container(height=10),
                        room_number,
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            "Confirmar Pedido",
                            on_click=submit_room_service_order,
                            style=ft.ButtonStyle(bgcolor=COLOR_AMBER_700, color=COLOR_WHITE, padding=ft.padding.all(15)),
                        ),
                    ], spacing=5),
                    padding=30,
                ),
                elevation=3,
            ),
        ], spacing=10, scroll=ft.ScrollMode.AUTO, expand=True)

    def update_cart_quantity(e, item_id, change):
        nonlocal room_service_cart
        for item in room_service_cart:
            if item['id'] == item_id:
                item['quantity'] += change
                if item['quantity'] <= 0:
                    room_service_cart.remove(item)
                break
        update_view()

    def remove_from_cart(e, item_id):
        nonlocal room_service_cart
        room_service_cart = [item for item in room_service_cart if item['id'] != item_id]
        page.snack_bar = ft.SnackBar(
            content=ft.Text("Item eliminado del carrito"),
            bgcolor=COLOR_GREEN,
        )
        page.snack_bar.open = True
        page.update()
        update_view()

    def create_room_service_confirmation_view():
        if not current_room_service_order:
            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ERROR, size=100, color=COLOR_RED_400),
                        ft.Container(height=20),
                        ft.Text("Error en el Pedido", size=30, weight=ft.FontWeight.BOLD),
                        ft.Container(height=10),
                        ft.Text("No se pudo procesar el pedido. Por favor intente nuevamente.", size=18),
                        ft.Container(height=30),
                        ft.ElevatedButton("Volver al inicio", on_click=lambda e: navigate(e, "home"), style=ft.ButtonStyle(bgcolor=COLOR_BLUE_900, color=COLOR_WHITE, padding=ft.padding.all(15))),
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.all(50), alignment=ft.alignment.center,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True)
        
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=100, color=COLOR_GREEN),
                    ft.Container(height=20),
                    ft.Text("¡Pedido Confirmado!", size=30, weight=ft.FontWeight.BOLD),
                    ft.Container(height=10),
                    ft.Text("Su pedido de servicio a la habitacion ha sido procesado con éxito.", size=18),
                    ft.Container(height=30),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.Text("Detalles del Pedido", size=20, weight=ft.FontWeight.BOLD),
                                ft.Container(height=10),
                                ft.Text(f"Número de Pedido: #{current_room_service_order['id']:04d}", size=16, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                                ft.Text(f"Cliente: {current_room_service_order['customer_name']}", size=16),
                                ft.Text(f"Habitación: {current_room_service_order['room_number']}", size=16),
                                ft.Container(height=10),
                                ft.Text("Items Pedidos:", size=16, weight=ft.FontWeight.BOLD),
                                ft.Column([
                                    ft.Text(f"• {item['name']} x{item['quantity']} - ${item['price'] * item['quantity']}", size=14)
                                    for item in current_room_service_order['items']
                                ], spacing=2),
                                ft.Container(height=5),
                                ft.Divider(height=1, color=COLOR_GREY_400),
                                ft.Container(height=5),
                                ft.Text(f"Total: ${current_room_service_order['total_price']}", size=18, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                            ], spacing=10),
                            padding=30,
                        ),
                        elevation=3,
                    ),
                    ft.Container(height=30),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("🕐 Tiempo Estimado de Entrega", size=16, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                            ft.Text("30-45 minutos", size=14, weight=ft.FontWeight.BOLD),
                            ft.Text("Nuestro equipo preparará su pedido con el mayor cuidado", size=12, color=COLOR_GREY_700),
                        ], spacing=5),
                        padding=15, bgcolor=COLOR_GREY_100, border_radius=10,
                    ),
                    ft.Container(height=20),
                    ft.Row([
                        ft.ElevatedButton("Volver al inicio", on_click=lambda e: navigate(e, "home"), style=ft.ButtonStyle(bgcolor=COLOR_BLUE_900, color=COLOR_WHITE, padding=ft.padding.all(15))),
                        ft.Container(width=20),
                        ft.ElevatedButton("Hacer otro pedido", on_click=lambda e: navigate(e, "room_service"), style=ft.ButtonStyle(bgcolor=COLOR_AMBER_700, color=COLOR_WHITE, padding=ft.padding.all(15))),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(50), alignment=ft.alignment.center,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True)

    def create_contact_view():
        contact_name = ft.TextField(
            label="Nombre completo", 
            border=ft.InputBorder.OUTLINE,
            width=400
        )
        contact_email = ft.TextField(
            label="Correo electrónico", 
            border=ft.InputBorder.OUTLINE,
            width=400
        )
        contact_phone = ft.TextField(
            label="Número de teléfono", 
            border=ft.InputBorder.OUTLINE,
            width=400
        )
        contact_message = ft.TextField(
            label="Dudas, consultas o comentarios",
            border=ft.InputBorder.OUTLINE,
            multiline=True,
            min_lines=5,
            max_lines=10,
            width=400,
            height=150
        )
        
        def submit_contact_form(e):
            if not contact_name.value or not contact_name.value.strip():
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Por favor ingrese su nombre completo"),
                    bgcolor=COLOR_RED_400,
                )
                page.snack_bar.open = True
                page.update()
                return
            
            if not contact_email.value or not contact_email.value.strip():
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Por favor ingrese su correo electrónico"),
                    bgcolor=COLOR_RED_400,
                )
                page.snack_bar.open = True
                page.update()
                return
            
            if "@" not in contact_email.value or "." not in contact_email.value:
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Por favor ingrese un correo electrónico válido"),
                    bgcolor=COLOR_RED_400,
                )
                page.snack_bar.open = True
                page.update()
                return
            
            if not contact_phone.value or not contact_phone.value.strip():
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Por favor ingrese su número de teléfono"),
                    bgcolor=COLOR_RED_400,
                )
                page.snack_bar.open = True
                page.update()
                return
            
            if not contact_message.value or not contact_message.value.strip():
                page.snack_bar = ft.SnackBar(
                    content=ft.Text("Por favor escriba su consulta o comentario"),
                    bgcolor=COLOR_RED_400,
                )
                page.snack_bar.open = True
                page.update()
                return
            
            name = contact_name.value.strip()
            email = contact_email.value.strip()
            phone = contact_phone.value.strip()
            message = contact_message.value.strip()
            
            nonlocal contact_confirmation_data
            contact_confirmation_data = {
                'name': name,
                'email': email,
                'phone': phone,
                'message': message
            }

            print("📞 FORMULARIO DE CONTACTO RECIBIDO:")
            print(f"👤 Nombre: {name}")
            print(f"📧 Email: {email}")
            print(f"📱 Teléfono: {phone}")
            print(f"💬 Mensaje: {message}")
            print("=" * 50)

            # Enviar email de confirmación
            success, message_result = email_service.send_contact_confirmation(name, email, phone, message)
            
            if success:
                print(f"✅ Email de confirmación enviado a {email}")
            else:
                print(f"❌ Error al enviar email: {message_result}")

            nonlocal current_view
            current_view = "contact_confirmation"
            update_view()

        def clear_form(e):
            contact_name.value = ""
            contact_email.value = ""
            contact_phone.value = ""
            contact_message.value = ""
            page.update()

        return ft.Column([
            ft.Container(
                content=ft.Text("Contacto", size=30, weight=ft.FontWeight.BOLD),
                alignment=ft.alignment.center,
                padding=ft.padding.only(top=30, bottom=20),
            ),
            
            ft.Container(
                content=ft.Row([
                    # Información de contacto
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Información de Contacto", size=24, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                            ft.Container(height=15),
                            ft.Row([
                                ft.Icon(ft.Icons.LOCATION_ON, color=COLOR_BLUE_900, size=20),
                                ft.Text("Av. Duarte Quiros 1205, Cordoba Capital, Argentina", size=16),
                            ], spacing=10),
                            ft.Container(height=10),
                            ft.Row([
                                ft.Icon(ft.Icons.PHONE, color=COLOR_BLUE_900, size=20),
                                ft.Text("+54 351 237-9493", size=16),
                            ], spacing=10),
                            ft.Container(height=10),
                            ft.Row([
                                ft.Icon(ft.Icons.EMAIL, color=COLOR_BLUE_900, size=20),
                                ft.Text("soporte.coflita@gmail.com", size=16),
                            ], spacing=10),
                            ft.Container(height=10),
                            ft.Row([
                                ft.Icon(ft.Icons.ACCESS_TIME, color=COLOR_BLUE_900, size=20),
                                ft.Text("Atención: 24/7", size=16),
                            ], spacing=10),
                        ], spacing=5),
                        padding=30,
                        bgcolor=COLOR_GREY_100,
                        border_radius=10,
                        width=400,
                    ),
                    
                    ft.Container(width=40),
                    
                    # Formulario de contacto
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Envíanos tu Consulta", size=24, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                            ft.Container(height=15),
                            ft.Text("Completa el formulario y nos pondremos en contacto contigo lo antes posible.", size=14, color=COLOR_GREY_700),
                            ft.Container(height=20),
                            
                            contact_name,
                            ft.Container(height=15),
                            contact_email,
                            ft.Container(height=15),
                            contact_phone,
                            ft.Container(height=15),
                            contact_message,
                            ft.Container(height=25),
                            
                            ft.Row([
                                ft.ElevatedButton(
                                    "Enviar Consulta",
                                    on_click=submit_contact_form,
                                    style=ft.ButtonStyle(
                                        bgcolor=COLOR_BLUE_900,
                                        color=COLOR_WHITE,
                                        padding=ft.padding.all(15),
                                    ),
                                    width=180,
                                ),
                                ft.Container(width=15),
                                ft.OutlinedButton(
                                    "Limpiar",
                                    on_click=clear_form,
                                    style=ft.ButtonStyle(
                                        color=COLOR_GREY_700,
                                        padding=ft.padding.all(15),
                                    ),
                                    width=120,
                                ),
                            ], alignment=ft.MainAxisAlignment.START),
                        ], spacing=5),
                        padding=30,
                        bgcolor=COLOR_WHITE,
                        border_radius=10,
                        width=500,
                        shadow=ft.BoxShadow(
                            spread_radius=1,
                            blur_radius=10,
                            color="#E0E0E0",
                            offset=ft.Offset(0, 2),
                        ),
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.padding.all(40),
            ),
            
            # Preguntas frecuentes
            ft.Container(
                content=ft.Column([
                    ft.Text("Preguntas Frecuentes", size=24, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                    ft.Container(height=20),
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text("¿Cuál es el horario de check-in?", size=16, weight=ft.FontWeight.BOLD),
                                ft.Text("El check-in es a partir de las 15:00 hrs.", size=14, color=COLOR_GREY_700),
                            ], spacing=5),
                            padding=20,
                            bgcolor=COLOR_GREY_100,
                            border_radius=10,
                            width=350,
                        ),
                        ft.Container(width=20),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("¿Incluye desayuno?", size=16, weight=ft.FontWeight.BOLD),
                                ft.Text("Sí, todas nuestras habitaciones incluyen desayuno buffet.", size=14, color=COLOR_GREY_700),
                            ], spacing=5),
                            padding=20,
                            bgcolor=COLOR_GREY_100,
                            border_radius=10,
                            width=350,
                        ),
                        ft.Container(width=20),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("¿Hay estacionamiento?", size=16, weight=ft.FontWeight.BOLD),
                                ft.Text("Sí, contamos con estacionamiento gratuito para huéspedes.", size=14, color=COLOR_GREY_700),
                            ], spacing=5),
                            padding=20,
                            bgcolor=COLOR_GREY_100,
                            border_radius=10,
                            width=350,
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(40),
                bgcolor=COLOR_WHITE,
            ),
        ], spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)

    def create_contact_confirmation_view():
        if not contact_confirmation_data:
            return ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ERROR, size=100, color=COLOR_RED_400),
                        ft.Container(height=20),
                        ft.Text("Error", size=30, weight=ft.FontWeight.BOLD),
                        ft.Container(height=10),
                        ft.Text("No se encontraron datos de la consulta.", size=18),
                        ft.Container(height=30),
                        ft.ElevatedButton("Volver al inicio", on_click=lambda e: navigate(e, "home"), style=ft.ButtonStyle(bgcolor=COLOR_BLUE_900, color=COLOR_WHITE, padding=ft.padding.all(15))),
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.padding.all(50), alignment=ft.alignment.center,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True)
        
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=120, color=COLOR_GREEN),
                    ft.Container(height=30),
                    ft.Text("¡Consulta Enviada!", size=32, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                    ft.Container(height=20),
                    ft.Text(
                        "Tu consulta se ha enviado al correo soporte.coflita@gmail.com",
                        size=18,
                        text_align=ft.TextAlign.CENTER,
                        color=COLOR_GREY_700
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "Por favor espere pacientemente a su respuesta",
                        size=16,
                        text_align=ft.TextAlign.CENTER,
                        color=COLOR_GREY_700
                    ),
                    ft.Container(height=40),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("📧 Detalles de tu consulta:", size=16, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                            ft.Container(height=10),
                            ft.Text(f"Nombre: {contact_confirmation_data['name']}", size=14),
                            ft.Text(f"Email: {contact_confirmation_data['email']}", size=14),
                            ft.Text(f"Teléfono: {contact_confirmation_data['phone']}", size=14),
                            ft.Container(height=10),
                            ft.Text("Tiempo estimado de respuesta: 24-48 horas", size=14, color=COLOR_AMBER_700, weight=ft.FontWeight.BOLD),
                        ], spacing=5),
                        padding=20,
                        bgcolor=COLOR_GREY_100,
                        border_radius=10,
                        width=500,
                    ),
                    
                    ft.Container(height=40),
                    ft.Row([
                        ft.ElevatedButton(
                            "Volver al Inicio",
                             on_click=lambda e: navigate(e, "home"),
                            style=ft.ButtonStyle(bgcolor=COLOR_BLUE_900, color=COLOR_WHITE, padding=ft.padding.all(15)),
                            width=180
                        ),
                        ft.Container(width=20),
                        ft.ElevatedButton(
                            "Enviar otra Consulta",
                             on_click=lambda e: navigate(e, "contact"),
                            style=ft.ButtonStyle(bgcolor=COLOR_AMBER_700, color=COLOR_WHITE, padding=ft.padding.all(15)),
                            width=180
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.padding.all(50),
                 alignment=ft.alignment.center,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True)

    def create_comments_view():
        # Variables para el formulario
        name_field = ft.TextField(
            label="Tu nombre",
            border=ft.InputBorder.UNDERLINE,
            width=300
        )
        
        category_dropdown = ft.Dropdown(
            label="Categoría",
            width=300,
            options=[
                ft.dropdown.Option("comidas", "🍽️ Comidas"),
                ft.dropdown.Option("habitaciones", "🛏️ Habitaciones"),
                ft.dropdown.Option("alquiler_autos", "🚗 Alquiler de Autos"),
                ft.dropdown.Option("hotel_general", "🏨 Hotel en General"),
            ]
        )
        
        rating_dropdown = ft.Dropdown(
            label="Calificación",
            width=300,
            options=[
                ft.dropdown.Option(1, "⭐"),
                ft.dropdown.Option(2, "⭐⭐"),
                ft.dropdown.Option(3, "⭐⭐⭐"),
                ft.dropdown.Option(4, "⭐⭐⭐⭐"),
                ft.dropdown.Option(5, "⭐⭐⭐⭐⭐"),
            ]
        )
        
        comment_field = ft.TextField(
            label="Tu comentario",
            border=ft.InputBorder.UNDERLINE,
            width=400,
            height=100,
            multiline=True,
            min_lines=3,
            max_lines=5
        )
        
        def submit_comment_form(e):
            if not name_field.value or not category_dropdown.value or not rating_dropdown.value or not comment_field.value:
                page.show_snack_bar(ft.SnackBar(content=ft.Text("Por favor completa todos los campos"), bgcolor=COLOR_RED_400))
                return
            
            # Agregar el comentario
            new_comment = comment_service.add_comment(
                category_dropdown.value,
                name_field.value,
                rating_dropdown.value,
                comment_field.value
            )
            
            # Guardar datos para la confirmación
            nonlocal comment_confirmation_data
            comment_confirmation_data = new_comment
            
            # Navegar a la confirmación
            navigate(e, "comment_confirmation")
        
        def clear_comment_form(e):
            name_field.value = ""
            category_dropdown.value = None
            rating_dropdown.value = None
            comment_field.value = ""
            name_field.update()
            category_dropdown.update()
            rating_dropdown.update()
            comment_field.update()
        
        # Obtener estadísticas
        total_comments = comment_service.get_comments_count()
        avg_comidas = comment_service.get_average_rating_by_category("comidas")
        avg_habitaciones = comment_service.get_average_rating_by_category("habitaciones")
        avg_autos = comment_service.get_average_rating_by_category("alquiler_autos")
        avg_general = comment_service.get_average_rating_by_category("hotel_general")
        
        # Crear sección de estadísticas
        stats_section = ft.Container(
            content=ft.Column([
                ft.Text("📊 Estadísticas de Comentarios", size=24, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                ft.Container(height=20),
                ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Total de comentarios", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(str(total_comments), size=24, color=COLOR_AMBER_700, weight=ft.FontWeight.BOLD),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        bgcolor=COLOR_GREY_100,
                        border_radius=10,
                        expand=True
                    ),
                    ft.Container(width=20),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("🍽️ Comidas", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{avg_comidas} ⭐" if avg_comidas > 0 else "Sin calificaciones", size=20, color=COLOR_AMBER_700),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        bgcolor=COLOR_GREY_100,
                        border_radius=10,
                        expand=True
                    ),
                    ft.Container(width=20),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("🛏️ Habitaciones", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{avg_habitaciones} ⭐" if avg_habitaciones > 0 else "Sin calificaciones", size=20, color=COLOR_AMBER_700),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        bgcolor=COLOR_GREY_100,
                        border_radius=10,
                        expand=True
                    ),
                    ft.Container(width=20),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("🚗 Alquiler Autos", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{avg_autos} ⭐" if avg_autos > 0 else "Sin calificaciones", size=20, color=COLOR_AMBER_700),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        bgcolor=COLOR_GREY_100,
                        border_radius=10,
                        expand=True
                    ),
                    ft.Container(width=20),
                    ft.Container(
                        content=ft.Column([
                            ft.Text("🏨 Hotel General", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{avg_general} ⭐" if avg_general > 0 else "Sin calificaciones", size=20, color=COLOR_AMBER_700),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        padding=20,
                        bgcolor=COLOR_GREY_100,
                        border_radius=10,
                        expand=True
                    ),
                ]),
            ]),
            padding=20,
            bgcolor=COLOR_WHITE,
            border_radius=10,
            margin=ft.margin.only(bottom=30)
        )
        
        # Crear formulario
        form_section = ft.Container(
            content=ft.Column([
                ft.Text("💬 Deja tu Comentario", size=24, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                ft.Container(height=20),
                ft.Row([
                    ft.Column([
                        name_field,
                        ft.Container(height=20),
                        category_dropdown,
                    ]),
                    ft.Container(width=40),
                    ft.Column([
                        rating_dropdown,
                        ft.Container(height=20),
                        comment_field,
                    ]),
                ]),
                ft.Container(height=30),
                ft.Row([
                    ft.ElevatedButton(
                        "Enviar Comentario",
                        on_click=submit_comment_form,
                        style=ft.ButtonStyle(bgcolor=COLOR_AMBER_700, color=COLOR_WHITE, padding=ft.padding.all(15)),
                        width=200
                    ),
                    ft.Container(width=20),
                    ft.ElevatedButton(
                        "Limpiar Formulario",
                        on_click=clear_comment_form,
                        style=ft.ButtonStyle(bgcolor=COLOR_GREY_400, color=COLOR_WHITE, padding=ft.padding.all(15)),
                        width=200
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
            ]),
            padding=30,
            bgcolor=COLOR_WHITE,
            border_radius=10,
            margin=ft.margin.only(bottom=30)
        )
        
        # Crear sección de comentarios existentes
        existing_comments = comment_service.get_all_comments()
        comments_section = ft.Container(
            content=ft.Column([
                ft.Text("📝 Comentarios Existentes", size=24, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                ft.Container(height=20),
                *[ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"📅 {comment['date']}", size=12, color=COLOR_GREY_700),
                            ft.Container(expand=True),
                            ft.Text(f"👤 {comment['name']}", size=14, weight=ft.FontWeight.BOLD),
                            ft.Container(width=10),
                            ft.Text("⭐" * comment['rating'], size=16, color=COLOR_AMBER_700),
                        ]),
                        ft.Container(height=5),
                        ft.Text(f"📂 {comment['category'].replace('_', ' ').title()}", size=12, color=COLOR_BLUE_700),
                        ft.Container(height=10),
                        ft.Text(comment['comment'], size=14),
                    ]),
                    padding=20,
                    bgcolor=COLOR_GREY_100,
                    border_radius=10,
                    margin=ft.margin.only(bottom=15)
                ) for comment in existing_comments]
            ]),
            padding=20,
            bgcolor=COLOR_WHITE,
            border_radius=10
        )
        
        return ft.Column([
            ft.Container(
                content=ft.Text("💬 Sección de Comentarios", size=32, weight=ft.FontWeight.BOLD, color=COLOR_WHITE),
                bgcolor=COLOR_BLUE_900,
                padding=30,
                alignment=ft.alignment.center,
            ),
            ft.Container(height=30),
            stats_section,
            form_section,
            comments_section,
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True)

    def create_comment_confirmation_view():
        if not comment_confirmation_data:
            return ft.Text("Error: No hay datos de confirmación")
        
        return ft.Column([
            ft.Container(
                content=ft.Text("✅ Comentario Enviado", size=32, weight=ft.FontWeight.BOLD, color=COLOR_WHITE),
                bgcolor=COLOR_GREEN,
                padding=30,
                alignment=ft.alignment.center,
            ),
            ft.Container(height=50),
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CHECK_CIRCLE, size=60, color=COLOR_GREEN),
                    ft.Container(height=20),
                    ft.Text("¡Gracias por tu comentario!", size=24, weight=ft.FontWeight.BOLD, color=COLOR_BLUE_900),
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"📂 Categoría: {comment_confirmation_data['category'].replace('_', ' ').title()}", size=16),
                            ft.Text(f"👤 Nombre: {comment_confirmation_data['name']}", size=16),
                            ft.Text(f"⭐ Calificación: {'⭐' * comment_confirmation_data['rating']}", size=16),
                            ft.Text(f"💬 Comentario: {comment_confirmation_data['comment']}", size=16),
                            ft.Text(f"📅 Fecha: {comment_confirmation_data['date']}", size=16),
                        ], spacing=5),
                        padding=20,
                        bgcolor=COLOR_GREY_100,
                        border_radius=10,
                        width=500,
                    ),
                    ft.Container(height=30),
                    ft.Text("Tu comentario ha sido registrado exitosamente.", size=16, color=COLOR_GREY_700),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                padding=20,
                bgcolor=COLOR_WHITE,
                border_radius=10,
                width=600,
            ),
            ft.Container(height=40),
            ft.Row([
                ft.ElevatedButton(
                    "Volver a Comentarios",
                    on_click=lambda e: navigate(e, "comments"),
                    style=ft.ButtonStyle(bgcolor=COLOR_BLUE_900, color=COLOR_WHITE, padding=ft.padding.all(15)),
                    width=200
                ),
                ft.Container(width=20),
                ft.ElevatedButton(
                    "Ir al Inicio",
                    on_click=lambda e: navigate(e, "home"),
                    style=ft.ButtonStyle(bgcolor=COLOR_AMBER_700, color=COLOR_WHITE, padding=ft.padding.all(15)),
                    width=200
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO, expand=True)

    # Initialize the scrollable content area once
    scrollable_content_area = ft.Container(content=ft.Text("Cargando..."), alignment=ft.alignment.center, padding=20, expand=True)

    # The main content container that holds nav_bar, scrollable_content_area, and footer
    # This container is created ONCE
    content_container = ft.Container(
        content=ft.Column([
            nav_bar, # This is the persistent nav_bar
            scrollable_content_area, # This is the persistent scrollable_content_area
            footer,
        ], spacing=0, scroll=ft.ScrollMode.AUTO),
        width=page.window_width, height=page.window_height,
    )

    def update_view():
        # Dialogs are now added once to page.overlay at the start,
        # so we only need to manage their 'open' property.
        
        if current_view == "home":
            view_content = create_home_view()
        elif current_view == "rooms":
            view_content = create_rooms_view()
        elif current_view == "room_details":
            view_content = create_room_details_view()
        elif current_view == "booking_confirmation":
            view_content = create_booking_confirmation_view()
        elif current_view == "room_comparison":
            view_content = create_room_comparison_view()
        elif current_view == "car_rental":
            view_content = create_car_rental_view()
        elif current_view == "car_details":
            view_content = create_car_details_view()
        elif current_view == "car_rental_confirmation":
            view_content = create_car_rental_confirmation_view()
        elif current_view == "room_service":
            view_content = create_room_service_view()
        elif current_view == "room_service_cart":
            view_content = create_room_service_cart_view()
        elif current_view == "room_service_confirmation":
            view_content = create_room_service_confirmation_view()
        elif current_view == "contact":
            view_content = create_contact_view()
        elif current_view == "contact_confirmation":
            view_content = create_contact_confirmation_view()
        elif current_view == "comments":
            view_content = create_comments_view()
        elif current_view == "comment_confirmation":
            view_content = create_comment_confirmation_view()
        else:
            view_content = ft.Text("Página no encontrada")
        
        scrollable_content_area.content = view_content
        scrollable_content_area.update() # Explicitly update the scrollable_content_area
        page.update()

    # Add the main content container to the page ONCE
    page.add(content_container)
    
    # Initial view update
    update_view()

if __name__ == "__main__":
    ft.app(target=main)
    print("🚀 Aplicación de Hotel Coflita iniciada")
    print("📧 Servicio de email configurado - Listo para envío real")
    print("🚗 Sistema de alquiler de autos disponible")
    print("🍽️ Servicio a la habitacion con carrito de compras")
    print("⚖️ Comparador de habitaciones implementado")
    print("💡 Para activar envío real de emails, cambia email_service.test_mode = False")
