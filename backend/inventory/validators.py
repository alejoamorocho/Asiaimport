from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re
from datetime import date

def validate_reference_number(value):
    """
    Valida que el número de referencia tenga el formato correcto: IMP-YYYY-XXX
    donde YYYY es el año y XXX es un número secuencial de 3 dígitos
    """
    pattern = r'^IMP-\d{4}-\d{3}$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('%(value)s no es un número de referencia válido. Debe tener el formato IMP-YYYY-XXX'),
            params={'value': value},
        )
    
    # Validar que el año en la referencia coincida con el año actual
    year = int(value.split('-')[1])
    if year != date.today().year:
        raise ValidationError(
            _('El año en la referencia debe ser el año actual'),
        )

def validate_serial_number(value):
    """
    Valida que el número de serie tenga el formato correcto según el tipo de producto
    """
    valid_prefixes = ['LPX1-', 'RF3K-', 'UCP-']  # Prefijos válidos según los productos
    
    if not any(value.startswith(prefix) for prefix in valid_prefixes):
        raise ValidationError(
            _('El número de serie debe comenzar con uno de los siguientes prefijos: %(prefixes)s'),
            params={'prefixes': ', '.join(valid_prefixes)},
        )
    
    # Validar el formato completo: PREFIJO-YYYY-XXX
    pattern = r'^[A-Z0-9]+-\d{4}-\d{3}$'
    if not re.match(pattern, value):
        raise ValidationError(
            _('El número de serie debe tener el formato PREFIJO-YYYY-XXX'),
        )

def validate_specifications(value):
    """
    Valida que las especificaciones contengan todos los campos requeridos
    y que los valores sean del tipo correcto
    """
    required_fields = {'potencia', 'peso', 'dimensiones', 'voltaje', 'frecuencia'}
    
    if not isinstance(value, dict):
        raise ValidationError(_('Las especificaciones deben ser un diccionario'))
    
    missing_fields = required_fields - set(value.keys())
    if missing_fields:
        raise ValidationError(
            _('Faltan los siguientes campos requeridos: %(fields)s'),
            params={'fields': ', '.join(missing_fields)},
        )
    
    # Validar que los valores no estén vacíos
    empty_fields = [field for field, val in value.items() if not str(val).strip()]
    if empty_fields:
        raise ValidationError(
            _('Los siguientes campos no pueden estar vacíos: %(fields)s'),
            params={'fields': ', '.join(empty_fields)},
        )
    
    # Validar tipos y rangos de valores específicos
    try:
        # Validar potencia (debe ser un número positivo)
        if not isinstance(value['potencia'], (int, float)) or value['potencia'] <= 0:
            raise ValidationError(_('La potencia debe ser un número positivo'))
        
        # Validar peso (debe ser un número positivo)
        if not isinstance(value['peso'], (int, float)) or value['peso'] <= 0:
            raise ValidationError(_('El peso debe ser un número positivo'))
        
        # Validar dimensiones (debe ser una cadena en formato LxAxH)
        if not re.match(r'^\d+x\d+x\d+$', str(value['dimensiones'])):
            raise ValidationError(_('Las dimensiones deben estar en formato LxAxH (ejemplo: 50x30x20)'))
        
        # Validar voltaje (debe ser un número positivo)
        if not isinstance(value['voltaje'], (int, float)) or value['voltaje'] <= 0:
            raise ValidationError(_('El voltaje debe ser un número positivo'))
        
        # Validar frecuencia (debe ser 50 o 60 Hz)
        if value['frecuencia'] not in [50, 60]:
            raise ValidationError(_('La frecuencia debe ser 50 o 60 Hz'))
            
    except KeyError as e:
        raise ValidationError(_('Campo requerido no encontrado: %(field)s'), params={'field': str(e)})
    except (TypeError, ValueError):
        raise ValidationError(_('Valor inválido en las especificaciones'))

def validate_import_date(value):
    """
    Valida que la fecha de importación no sea futura
    """
    if value > date.today():
        raise ValidationError(
            _('La fecha de importación no puede ser futura'),
        )

def validate_received_quantity(value, expected_quantity):
    """
    Valida que la cantidad recibida no exceda la cantidad esperada y sea un número positivo
    """
    if not isinstance(value, int):
        raise ValidationError(_('La cantidad recibida debe ser un número entero'))
        
    if value < 0:
        raise ValidationError(_('La cantidad recibida no puede ser negativa'))
        
    if value > expected_quantity:
        raise ValidationError(
            _('La cantidad recibida (%(value)d) no puede ser mayor que la cantidad esperada (%(expected)d)'),
            params={'value': value, 'expected': expected_quantity},
        )

def validate_status_transition(old_status, new_status):
    """
    Valida las transiciones permitidas entre estados de una unidad de producto
    """
    ALLOWED_TRANSITIONS = {
        'available': {'in_use', 'maintenance', 'defective'},
        'in_use': {'available', 'maintenance', 'defective'},
        'maintenance': {'available', 'defective', 'disposed'},
        'defective': {'maintenance', 'disposed'},
        'disposed': set()  # No se permite transición desde disposed
    }
    
    if old_status == new_status:
        return
        
    if new_status not in ALLOWED_TRANSITIONS.get(old_status, set()):
        raise ValidationError(
            _('Transición de estado no permitida: de %(old)s a %(new)s'),
            params={'old': old_status, 'new': new_status},
        )
