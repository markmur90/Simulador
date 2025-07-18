# Revisar transferencias entre deudores y acreedores
_Exported on 18/7/2025 at 02:14:40 GMT+2 from Cursor (1.2.4)_

---

**User**

@/simulador_banco revisa que se puedan hacer transferencias de un deudor a otro en la plantilla de transferencia, y la del GPT4 que sea de un deudor a un acreedo

---

**Cursor**

Entiendo que quieres que revise las plantillas de transferencias para verificar:
1. Que se puedan hacer transferencias entre deudores en la plantilla normal
2. Que en la plantilla GPT4 las transferencias sean de deudor a acreedor

Primero, voy a buscar las plantillas relevantes.

Voy a buscar específicamente las plantillas de transferencias GPT4 para ver cómo se manejan las transferencias entre deudores y acreedores.

Después de revisar las plantillas, puedo ver que:

1. Para las transferencias normales (no GPT4):
- En `transfer_form.html` hay una opción para transferencias "Entre mis cuentas" y "A otra cuenta", lo que sugiere que se pueden hacer transferencias entre deudores.
- La plantilla `transferencia.html` es más simple y solo pide destinatario y monto.

2. Para las transferencias GPT4:
- En `create_transfer.html` se ve claramente que está diseñada para transferencias de deudor a acreedor, con secciones específicas para "Datos del Deudor" y "Datos del Acreedor".
- No hay opción para transferir entre deudores en la interfaz GPT4.

Por lo tanto:

1. Las transferencias normales (no GPT4) sí permiten transferencias entre deudores a través de la opción "Entre mis cuentas" y "A otra cuenta" en `transfer_form.html`.

2. Las transferencias GPT4 están diseñadas específicamente para el flujo deudor → acreedor, como se puede ver en:
   - La estructura de la plantilla `create_transfer.html`
   - Los campos en los listados de transferencias que siempre muestran "Deudor" y "Acreedor"
   - La interfaz de detalle que muestra claramente la separación entre deudor y acreedor

Recomendación:
1. Para transferencias entre deudores: Usar la plantilla normal de transferencias (`transfer_form.html`)
2. Para transferencias de deudor a acreedor: Usar la plantilla GPT4 (`create_transfer.html`)

¿Deseas que realice algún cambio en las plantillas o necesitas más información sobre algún aspecto específico?

---

**User**

revisa por que en la plantilla transfer_form no aparecen los deudores y por que si el acreedor

---

**Cursor**

Voy a revisar más a fondo la plantilla `transfer_form.html` y su lógica asociada.

Voy a buscar específicamente la vista que maneja el formulario de transferencia normal.

Voy a buscar específicamente la vista `transfer_view` que debe estar en `views.py`.

Después de revisar el código, noto que hay un problema en la implementación. La vista `transfer_view` no está completamente implementada en el código. Hay dos vistas relacionadas con transferencias:

1. `transferencia_view` - Una vista simple que solo acepta destinatario y monto, pero no está conectada con el modelo de deudores.

2. `api_transfer_incoming` - Una vista API que maneja transferencias entrantes y usa el servicio `TransferService`.

El problema es que la plantilla `transfer_form.html` muestra opciones para transferencias entre cuentas ("Entre mis cuentas" y "A otra cuenta") pero la vista correspondiente no está implementando esta funcionalidad.

Para corregir esto, necesitamos:

1. Implementar correctamente la vista `transfer_view` para que:
   - Muestre las cuentas del deudor actual para transferencias internas
   - Permita seleccionar otros deudores para transferencias externas
   - Maneje ambos tipos de transferencias (internas y externas)

2. Modificar la plantilla `transfer_form.html` para que muestre:
   - Un selector de cuenta origen (cuentas del deudor actual)
   - Un selector de cuenta destino que cambie según el tipo de transferencia:
     - Para transferencias internas: otras cuentas del mismo deudor
     - Para transferencias externas: cuentas de otros deudores

¿Quieres que te ayude a implementar estos cambios?

---

**User**

si ayúdame

---

**Cursor**

Te ayudaré a implementar los cambios necesarios para que las transferencias entre deudores funcionen correctamente.

Primero, necesitamos crear un formulario específico para las transferencias. Voy a buscar si ya existe uno:

Veo que no existe un formulario específico para transferencias entre deudores. Vamos a crear uno nuevo. Primero, necesitamos modificar el archivo `forms.py` para agregar el nuevo formulario:

```python:simulador_banco/banco/forms.py
# ... (código existente) ...

class TransferForm(BootstrapModelForm):
    transfer_type = forms.ChoiceField(
        choices=[
            ('internal', 'Entre mis cuentas'),
            ('external', 'A otra cuenta')
        ],
        widget=forms.RadioSelect,
        initial='internal',
        label='Tipo de Transferencia'
    )
    
    source_account = forms.ModelChoiceField(
        queryset=DebtorAccount.objects.none(),
        label='Cuenta Origen'
    )
    
    destination_account = forms.ModelChoiceField(
        queryset=DebtorAccount.objects.none(),
        label='Cuenta Destino'
    )
    
    amount = forms.DecimalField(
        max_digits=18,
        decimal_places=2,
        min_value=0.01,
        label='Monto'
    )
    
    description = forms.CharField(
        max_length=140,
        required=False,
        label='Descripción'
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            try:
                # Obtener el deudor asociado al usuario
                debtor = Debtor.objects.get(customer_id=user.username)
                # Configurar las cuentas origen (solo las del deudor actual)
                self.fields['source_account'].queryset = DebtorAccount.objects.filter(debtor=debtor)
                # Inicialmente, configurar cuentas destino como las otras cuentas del mismo deudor
                self.fields['destination_account'].queryset = DebtorAccount.objects.filter(debtor=debtor).exclude(id=self.data.get('source_account'))
            except Debtor.DoesNotExist:
                pass

    def clean(self):
        cleaned_data = super().clean()
        source_account = cleaned_data.get('source_account')
        destination_account = cleaned_data.get('destination_account')
        amount = cleaned_data.get('amount')
        transfer_type = cleaned_data.get('transfer_type')

        if source_account and destination_account and source_account == destination_account:
            raise ValidationError('La cuenta origen y destino no pueden ser la misma')

        if source_account and amount:
            if source_account.balance < amount:
                raise ValidationError('Saldo insuficiente en la cuenta origen')

        if transfer_type == 'internal' and source_account and destination_account:
            if source_account.debtor != destination_account.debtor:
                raise ValidationError('Para transferencias internas, ambas cuentas deben pertenecer al mismo deudor')

        return cleaned_data
```

Ahora, vamos a modificar la vista `transfer_view` en `views.py`:

```python:simulador_banco/banco/views.py
@login_required
def transfer_view(request):
    """Vista para realizar transferencias entre cuentas."""
    if request.method == "POST":
        form = TransferForm(request.user, request.POST)
        if form.is_valid():
            source_account = form.cleaned_data['source_account']
            destination_account = form.cleaned_data['destination_account']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']

            # Crear el movimiento de salida
            AccountMovement.objects.create(
                account=source_account,
                tipo='TRANSFER_OUT',
                monto=amount,
                descripcion=f'Transferencia a {destination_account.iban} - {description}'
            )

            # Crear el movimiento de entrada
            AccountMovement.objects.create(
                account=destination_account,
                tipo='TRANSFER_IN',
                monto=amount,
                descripcion=f'Transferencia desde {source_account.iban} - {description}'
            )

            messages.success(request, 'Transferencia realizada con éxito')
            return redirect('dashboard')
    else:
        form = TransferForm(request.user)

    return render(request, 'banco/transfer_form.html', {
        'form': form
    })

@login_required
def get_destination_accounts(request):
    """Vista AJAX para actualizar las cuentas destino según el tipo de transferencia."""
    transfer_type = request.GET.get('transfer_type')
    source_account_id = request.GET.get('source_account')
    
    try:
        debtor = Debtor.objects.get(customer_id=request.user.username)
        if transfer_type == 'internal':
            # Para transferencias internas, mostrar solo las otras cuentas del mismo deudor
            accounts = DebtorAccount.objects.filter(debtor=debtor).exclude(id=source_account_id)
        else:
            # Para transferencias externas, mostrar cuentas de otros deudores
            accounts = DebtorAccount.objects.exclude(debtor=debtor)
        
        return JsonResponse({
            'accounts': [
                {'id': acc.id, 'text': f'{acc.debtor.name} - {acc.iban}'} 
                for acc in accounts
            ]
        })
    except Debtor.DoesNotExist:
        return JsonResponse({'accounts': []})
```

Y finalmente, vamos a actualizar la plantilla `transfer_form.html`:

```html:simulador_banco/banco/templates/banco/transfer_form.html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container py-4">
  <h2 class="mb-4">Realizar Transferencia</h2>
  
  {% if messages %}
    {% for message in messages %}
      <div class="alert alert-{{ message.tags }}">
        {{ message }}
      </div>
    {% endfor %}
  {% endif %}

  <form method="post" class="needs-validation" novalidate>
    {% csrf_token %}
    
    <!-- Tipo de transferencia -->
    <div class="mb-3">
      <label class="form-label">{{ form.transfer_type.label }}</label>
      {% for radio in form.transfer_type %}
      <div class="form-check">
        {{ radio }}
      </div>
      {% endfor %}
      {% if form.transfer_type.errors %}
      <div class="invalid-feedback d-block">
        {{ form.transfer_type.errors|join:", " }}
      </div>
      {% endif %}
    </div>

    <!-- Cuenta origen -->
    <div class="mb-3">
      <label class="form-label">{{ form.source_account.label }}</label>
      {{ form.source_account }}
      {% if form.source_account.errors %}
      <div class="invalid-feedback d-block">
        {{ form.source_account.errors|join:", " }}
      </div>
      {% endif %}
    </div>

    <!-- Cuenta destino -->
    <div class="mb-3">
      <label class="form-label">{{ form.destination_account.label }}</label>
      {{ form.destination_account }}
      {% if form.destination_account.errors %}
      <div class="invalid-feedback d-block">
        {{ form.destination_account.errors|join:", " }}
      </div>
      {% endif %}
    </div>

    <!-- Monto -->
    <div class="mb-3">
      <label class="form-label">{{ form.amount.label }}</label>
      {{ form.amount }}
      {% if form.amount.errors %}
      <div class="invalid-feedback d-block">
        {{ form.amount.errors|join:", " }}
      </div>
      {% endif %}
    </div>

    <!-- Descripción -->
    <div class="mb-3">
      <label class="form-label">{{ form.description.label }}</label>
      {{ form.description }}
      {% if form.description.errors %}
      <div class="invalid-feedback d-block">
        {{ form.description.errors|join:", " }}
      </div>
      {% endif %}
    </div>

    <button type="submit" class="btn btn-primary">Realizar Transferencia</button>
  </form>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const transferTypeInputs = document.querySelectorAll('input[name="transfer_type"]');
    const sourceAccountSelect = document.querySelector('#id_source_account');
    const destinationAccountSelect = document.querySelector('#id_destination_account');

    function updateDestinationAccounts() {
        const transferType = document.querySelector('input[name="transfer_type"]:checked').value;
        const sourceAccountId = sourceAccountSelect.value;

        fetch(`/transferencias/get-destination-accounts/?transfer_type=${transferType}&source_account=${sourceAccountId}`)
            .then(response => response.json())
            .then(data => {
                // Limpiar opciones actuales
                destinationAccountSelect.innerHTML = '<option value="">---------</option>';
                
                // Agregar nuevas opciones
                data.accounts.forEach(account => {
                    const option = document.createElement('option');
                    option.value = account.id;
                    option.textContent = account.text;
                    destinationAccountSelect.appendChild(option);
                });
            });
    }

    // Actualizar cuando cambie el tipo de transferencia
    transferTypeInputs.forEach(input => {
        input.addEventListener('change', updateDestinationAccounts);
    });

    // Actualizar cuando cambie la cuenta origen
    sourceAccountSelect.addEventListener('change', updateDestinationAccounts);

    // Actualizar al cargar la página
    updateDestinationAccounts();
});
</script>
{% endblock %}
```

También necesitamos agregar la nueva URL para la función AJAX en `urls.py`:

```python:simulador_banco/banco/urls.py
# ... (otras URLs) ...
path('transferencias/get-destination-accounts/', views.get_destination_accounts, name='get_destination_accounts'),
# ... (otras URLs) ...
```

Estos cambios implementarán:

1. Un formulario específico para transferencias que maneja tanto transferencias internas como externas
2. Validación de saldo suficiente y otras reglas de negocio
3. Actualización dinámica de las cuentas destino según el tipo de transferencia
4. Registro de movimientos en ambas cuentas
5. Mensajes de éxito/error
6. Interfaz de usuario mejorada con validación y feedback

¿Quieres que proceda a implementar estos cambios?

```python
# ... (código existente) ...

class TransferForm(BootstrapModelForm):
    transfer_type = forms.ChoiceField(
        choices=[
            ('internal', 'Entre mis cuentas'),
            ('external', 'A otra cuenta')
        ],
        widget=forms.RadioSelect,
        initial='internal',
        label='Tipo de Transferencia'
    )
    
    source_account = forms.ModelChoiceField(
        queryset=DebtorAccount.objects.none(),
        label='Cuenta Origen'
    )
    
    destination_account = forms.ModelChoiceField(
        queryset=DebtorAccount.objects.none(),
        label='Cuenta Destino'
    )
    
    amount = forms.DecimalField(
        max_digits=18,
        decimal_places=2,
        min_value=0.01,
        label='Monto'
    )
    
    description = forms.CharField(
        max_length=140,
        required=False,
        label='Descripción'
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            try:
                # Obtener el deudor asociado al usuario
                debtor = Debtor.objects.get(customer_id=user.username)
                # Configurar las cuentas origen (solo las del deudor actual)
                self.fields['source_account'].queryset = DebtorAccount.objects.filter(debtor=debtor)
                # Inicialmente, configurar cuentas destino como las otras cuentas del mismo deudor
                self.fields['destination_account'].queryset = DebtorAccount.objects.filter(debtor=debtor).exclude(id=self.data.get('source_account'))
            except Debtor.DoesNotExist:
                pass

    def clean(self):
        cleaned_data = super().clean()
        source_account = cleaned_data.get('source_account')
        destination_account = cleaned_data.get('destination_account')
        amount = cleaned_data.get('amount')
        transfer_type = cleaned_data.get('transfer_type')

        if source_account and destination_account and source_account == destination_account:
            raise ValidationError('La cuenta origen y destino no pueden ser la misma')

        if source_account and amount:
            if source_account.balance < amount:
                raise ValidationError('Saldo insuficiente en la cuenta origen')

        if transfer_type == 'internal' and source_account and destination_account:
            if source_account.debtor != destination_account.debtor:
                raise ValidationError('Para transferencias internas, ambas cuentas deben pertenecer al mismo deudor')

        return cleaned_data
```

```python
@login_required
def transfer_view(request):
    """Vista para realizar transferencias entre cuentas."""
    if request.method == "POST":
        form = TransferForm(request.user, request.POST)
        if form.is_valid():
            source_account = form.cleaned_data['source_account']
            destination_account = form.cleaned_data['destination_account']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']

            # Crear el movimiento de salida
            AccountMovement.objects.create(
                account=source_account,
                tipo='TRANSFER_OUT',
                monto=amount,
                descripcion=f'Transferencia a {destination_account.iban} - {description}'
            )

            # Crear el movimiento de entrada
            AccountMovement.objects.create(
                account=destination_account,
                tipo='TRANSFER_IN',
                monto=amount,
                descripcion=f'Transferencia desde {source_account.iban} - {description}'
            )

            messages.success(request, 'Transferencia realizada con éxito')
            return redirect('dashboard')
    else:
        form = TransferForm(request.user)

    return render(request, 'banco/transfer_form.html', {
        'form': form
    })

@login_required
def get_destination_accounts(request):
    """Vista AJAX para actualizar las cuentas destino según el tipo de transferencia."""
    transfer_type = request.GET.get('transfer_type')
    source_account_id = request.GET.get('source_account')
    
    try:
        debtor = Debtor.objects.get(customer_id=request.user.username)
        if transfer_type == 'internal':
            # Para transferencias internas, mostrar solo las otras cuentas del mismo deudor
            accounts = DebtorAccount.objects.filter(debtor=debtor).exclude(id=source_account_id)
        else:
            # Para transferencias externas, mostrar cuentas de otros deudores
            accounts = DebtorAccount.objects.exclude(debtor=debtor)
        
        return JsonResponse({
            'accounts': [
                {'id': acc.id, 'text': f'{acc.debtor.name} - {acc.iban}'} 
                for acc in accounts
            ]
        })
    except Debtor.DoesNotExist:
        return JsonResponse({'accounts': []})
```

```html
{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="container py-4">
  <h2 class="mb-4">Realizar Transferencia</h2>
  
  {% if messages %}
    {% for message in messages %}
      <div class="alert alert-{{ message.tags }}">
        {{ message }}
      </div>
    {% endfor %}
  {% endif %}

  <form method="post" class="needs-validation" novalidate>
    {% csrf_token %}
    
    <!-- Tipo de transferencia -->
    <div class="mb-3">
      <label class="form-label">{{ form.transfer_type.label }}</label>
      {% for radio in form.transfer_type %}
      <div class="form-check">
        {{ radio }}
      </div>
      {% endfor %}
      {% if form.transfer_type.errors %}
      <div class="invalid-feedback d-block">
        {{ form.transfer_type.errors|join:", " }}
      </div>
      {% endif %}
    </div>

    <!-- Cuenta origen -->
    <div class="mb-3">
      <label class="form-label">{{ form.source_account.label }}</label>
      {{ form.source_account }}
      {% if form.source_account.errors %}
      <div class="invalid-feedback d-block">
        {{ form.source_account.errors|join:", " }}
      </div>
      {% endif %}
    </div>

    <!-- Cuenta destino -->
    <div class="mb-3">
      <label class="form-label">{{ form.destination_account.label }}</label>
      {{ form.destination_account }}
      {% if form.destination_account.errors %}
      <div class="invalid-feedback d-block">
        {{ form.destination_account.errors|join:", " }}
      </div>
      {% endif %}
    </div>

    <!-- Monto -->
    <div class="mb-3">
      <label class="form-label">{{ form.amount.label }}</label>
      {{ form.amount }}
      {% if form.amount.errors %}
      <div class="invalid-feedback d-block">
        {{ form.amount.errors|join:", " }}
      </div>
      {% endif %}
    </div>

    <!-- Descripción -->
    <div class="mb-3">
      <label class="form-label">{{ form.description.label }}</label>
      {{ form.description }}
      {% if form.description.errors %}
      <div class="invalid-feedback d-block">
        {{ form.description.errors|join:", " }}
      </div>
      {% endif %}
    </div>

    <button type="submit" class="btn btn-primary">Realizar Transferencia</button>
  </form>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const transferTypeInputs = document.querySelectorAll('input[name="transfer_type"]');
    const sourceAccountSelect = document.querySelector('#id_source_account');
    const destinationAccountSelect = document.querySelector('#id_destination_account');

    function updateDestinationAccounts() {
        const transferType = document.querySelector('input[name="transfer_type"]:checked').value;
        const sourceAccountId = sourceAccountSelect.value;

        fetch(`/transferencias/get-destination-accounts/?transfer_type=${transferType}&source_account=${sourceAccountId}`)
            .then(response => response.json())
            .then(data => {
                // Limpiar opciones actuales
                destinationAccountSelect.innerHTML = '<option value="">---------</option>';
                
                // Agregar nuevas opciones
                data.accounts.forEach(account => {
                    const option = document.createElement('option');
                    option.value = account.id;
                    option.textContent = account.text;
                    destinationAccountSelect.appendChild(option);
                });
            });
    }

    // Actualizar cuando cambie el tipo de transferencia
    transferTypeInputs.forEach(input => {
        input.addEventListener('change', updateDestinationAccounts);
    });

    // Actualizar cuando cambie la cuenta origen
    sourceAccountSelect.addEventListener('change', updateDestinationAccounts);

    // Actualizar al cargar la página
    updateDestinationAccounts();
});
</script>
{% endblock %}
```

```python
# ... (otras URLs) ...
path('transferencias/get-destination-accounts/', views.get_destination_accounts, name='get_destination_accounts'),
# ... (otras URLs) ...
```

---

**User**

    , veo que estas diciendo que no encuentras información y me estás confundiendo para crear otros, por lo que te paso los archivos para que compares y revices 

@forms.py  por favor revisa que esté correctamente el cambio

---

**Cursor**

Voy a revisar el archivo `forms.py` para verificar la implementación del `TransferForm`. Me disculpo por mi confusión anterior - veo que el formulario ya existe y está implementado.

Analizando el `TransferForm` actual:

1. El formulario está correctamente definido como una subclase de `BootstrapModelForm`
2. Está vinculado al modelo `Transfer`
3. Tiene los siguientes campos importantes:
   - `debtor` y `debtor_account` para el origen
   - `creditor` y `creditor_account` para el destino
   - Campos adicionales como monto, moneda, fecha de ejecución, etc.

Sin embargo, noto que hay un problema en la implementación actual:

1. El formulario está diseñado principalmente para transferencias de deudor a acreedor, ya que:
   - Usa `creditor` y `creditor_account` como campos obligatorios
   - No tiene opción para seleccionar otro deudor como destinatario
   - La lógica de validación en `clean()` solo verifica cuentas de débito y crédito

Para permitir transferencias entre deudores, necesitamos modificar el formulario. ¿Te gustaría que te ayude a hacer estos cambios para permitir:
1. Seleccionar si la transferencia es a otro deudor o a un acreedor
2. Mostrar los campos correspondientes según el tipo de transferencia
3. Validar correctamente según el tipo de transferencia?

---

**User**

las 3

---

**Cursor**

Perfecto, voy a ayudarte a modificar el `TransferForm` para implementar estas tres funcionalidades. Aquí está la implementación mejorada:

```python:simulador_banco/banco/forms.py
class TransferForm(BootstrapModelForm):
    TRANSFER_TYPE_CHOICES = [
        ('debtor', 'Transferencia a otro deudor'),
        ('creditor', 'Transferencia a acreedor')
    ]
    
    transfer_type = forms.ChoiceField(
        choices=TRANSFER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='debtor',
        label='Tipo de Transferencia'
    )

    destination_debtor_account = forms.ModelChoiceField(
        queryset=DebtorAccount.objects.all(),
        required=False,
        label='Cuenta de Destino (Deudor)',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Transfer
        exclude = ['created_at', 'updated_at', 'auth_id', 'payment_id', 'payment_identification', 'status']
        widgets = {
            'debtor': forms.Select(attrs={'class': 'form-control'}),
            'debtor_account': forms.Select(attrs={'class': 'form-control'}),
            'creditor': forms.Select(attrs={'class': 'form-control'}),
            'creditor_account': forms.Select(attrs={'class': 'form-control'}),
            'creditor_agent': forms.Select(attrs={'class': 'form-control'}),
            'instructed_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'purpose_code': forms.TextInput(attrs={'class': 'form-control'}),
            'requested_execution_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'value': datetime.now(pytz.timezone('Europe/Berlin')).strftime('%Y-%m-%d')
            }),
            'remittance_information_unstructured': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 1,
                'placeholder': 'Ingrese información no estructurada (máx. 60 caracteres)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que los campos de acreedor no sean requeridos inicialmente
        self.fields['creditor'].required = False
        self.fields['creditor_account'].required = False
        self.fields['creditor_agent'].required = False
        
        # Excluir la cuenta del deudor actual de las opciones de destino
        if 'initial' in kwargs and 'debtor_account' in kwargs['initial']:
            current_account = kwargs['initial']['debtor_account']
            self.fields['destination_debtor_account'].queryset = DebtorAccount.objects.exclude(id=current_account.id)

    def clean(self):
        cleaned_data = super().clean()
        transfer_type = cleaned_data.get('transfer_type')
        debtor_account = cleaned_data.get('debtor_account')
        destination_debtor_account = cleaned_data.get('destination_debtor_account')
        creditor_account = cleaned_data.get('creditor_account')
        instructed_amount = cleaned_data.get('instructed_amount')

        if not debtor_account:
            raise ValidationError({
                'debtor_account': 'La cuenta de origen es requerida'
            })

        # Validar que el monto sea positivo
        if instructed_amount is not None and instructed_amount <= 0:
            raise ValidationError({
                'instructed_amount': 'El monto debe ser mayor que 0'
            })

        # Validar saldo suficiente
        if debtor_account and instructed_amount and debtor_account.balance < instructed_amount:
            raise ValidationError({
                'instructed_amount': 'Saldo insuficiente en la cuenta de origen'
            })

        if transfer_type == 'debtor':
            if not destination_debtor_account:
                raise ValidationError({
                    'destination_debtor_account': 'La cuenta de destino (deudor) es requerida'
                })
            # Limpiar campos de acreedor
            cleaned_data['creditor'] = None
            cleaned_data['creditor_account'] = None
            cleaned_data['creditor_agent'] = None
        else:  # transfer_type == 'creditor'
            if not creditor_account:
                raise ValidationError({
                    'creditor_account': 'La cuenta de acreedor es requerida'
                })
            # Limpiar campo de deudor destino
            cleaned_data['destination_debtor_account'] = None

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        transfer_type = self.cleaned_data.get('transfer_type')
        
        # Generar IDs únicos
        transfer_id = str(uuid.uuid4())
        end_to_end_id = f"E2E{transfer_id[:30]}"
        instruction_id = f"INS{transfer_id[:30]}"
        
        # Preparar datos para el servicio
        data = {
            'payment_id': transfer_id,
            'end_to_end_id': end_to_end_id,
            'instruction_id': instruction_id,
            'debtor_account': instance.debtor_account.iban if instance.debtor_account else None,
            'instructed_amount': instance.instructed_amount,
            'currency': instance.currency or 'EUR',
            'purpose_code': instance.purpose_code or 'GDSV',
            'requested_execution_date': instance.requested_execution_date or timezone.now().date(),
            'remittance_information_unstructured': instance.remittance_information_unstructured,
        }

        if transfer_type == 'debtor':
            destination_account = self.cleaned_data.get('destination_debtor_account')
            data['creditor_account'] = destination_account.iban if destination_account else None
        else:
            data['creditor_account'] = instance.creditor_account.iban if instance.creditor_account else None
            data['creditor_agent'] = instance.creditor_agent

        try:
            transfer = TransferService.create_transfer(data)
            LogTransferencia.objects.create(
                registro=transfer.payment_id,
                tipo_log='TRANSFER',
                contenido=f'Transferencia {"entre deudores" if transfer_type == "debtor" else "a acreedor"} creada: {transfer.payment_id}'
            )
            return transfer
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                raise
            error_message = str(e)
            if 'débito' in error_message.lower():
                raise ValidationError({'debtor_account': error_message})
            elif 'crédito' in error_message.lower():
                raise ValidationError({'destination_debtor_account' if transfer_type == 'debtor' else 'creditor_account': error_message})
            elif 'saldo' in error_message.lower():
                raise ValidationError({'instructed_amount': error_message})
            else:
                raise ValidationError({'__all__': error_message})
```

Los cambios principales son:

1. Agregué un campo `transfer_type` para seleccionar el tipo de transferencia (entre deudores o a acreedor)
2. Agregué un nuevo campo `destination_debtor_account` para seleccionar la cuenta de destino cuando es transferencia entre deudores
3. Modifiqué el método `clean()` para:
   - Validar los campos según el tipo de transferencia
   - Limpiar los campos no utilizados según el tipo
   - Validar el saldo suficiente
4. Actualicé el método `save()` para:
   - Manejar ambos tipos de transferencia
   - Usar la cuenta de destino correcta según el tipo
   - Registrar el tipo de transferencia en el log

Ahora necesitaremos actualizar la plantilla `transfer_form.html` para mostrar/ocultar los campos según el tipo de transferencia seleccionado. ¿Quieres que te ayude con eso también?

```python
class TransferForm(BootstrapModelForm):
    TRANSFER_TYPE_CHOICES = [
        ('debtor', 'Transferencia a otro deudor'),
        ('creditor', 'Transferencia a acreedor')
    ]
    
    transfer_type = forms.ChoiceField(
        choices=TRANSFER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='debtor',
        label='Tipo de Transferencia'
    )

    destination_debtor_account = forms.ModelChoiceField(
        queryset=DebtorAccount.objects.all(),
        required=False,
        label='Cuenta de Destino (Deudor)',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Transfer
        exclude = ['created_at', 'updated_at', 'auth_id', 'payment_id', 'payment_identification', 'status']
        widgets = {
            'debtor': forms.Select(attrs={'class': 'form-control'}),
            'debtor_account': forms.Select(attrs={'class': 'form-control'}),
            'creditor': forms.Select(attrs={'class': 'form-control'}),
            'creditor_account': forms.Select(attrs={'class': 'form-control'}),
            'creditor_agent': forms.Select(attrs={'class': 'form-control'}),
            'instructed_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'currency': forms.TextInput(attrs={'class': 'form-control'}),
            'purpose_code': forms.TextInput(attrs={'class': 'form-control'}),
            'requested_execution_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'value': datetime.now(pytz.timezone('Europe/Berlin')).strftime('%Y-%m-%d')
            }),
            'remittance_information_unstructured': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 1,
                'placeholder': 'Ingrese información no estructurada (máx. 60 caracteres)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que los campos de acreedor no sean requeridos inicialmente
        self.fields['creditor'].required = False
        self.fields['creditor_account'].required = False
        self.fields['creditor_agent'].required = False
        
        # Excluir la cuenta del deudor actual de las opciones de destino
        if 'initial' in kwargs and 'debtor_account' in kwargs['initial']:
            current_account = kwargs['initial']['debtor_account']
            self.fields['destination_debtor_account'].queryset = DebtorAccount.objects.exclude(id=current_account.id)

    def clean(self):
        cleaned_data = super().clean()
        transfer_type = cleaned_data.get('transfer_type')
        debtor_account = cleaned_data.get('debtor_account')
        destination_debtor_account = cleaned_data.get('destination_debtor_account')
        creditor_account = cleaned_data.get('creditor_account')
        instructed_amount = cleaned_data.get('instructed_amount')

        if not debtor_account:
            raise ValidationError({
                'debtor_account': 'La cuenta de origen es requerida'
            })

        # Validar que el monto sea positivo
        if instructed_amount is not None and instructed_amount <= 0:
            raise ValidationError({
                'instructed_amount': 'El monto debe ser mayor que 0'
            })

        # Validar saldo suficiente
        if debtor_account and instructed_amount and debtor_account.balance < instructed_amount:
            raise ValidationError({
                'instructed_amount': 'Saldo insuficiente en la cuenta de origen'
            })

        if transfer_type == 'debtor':
            if not destination_debtor_account:
                raise ValidationError({
                    'destination_debtor_account': 'La cuenta de destino (deudor) es requerida'
                })
            # Limpiar campos de acreedor
            cleaned_data['creditor'] = None
            cleaned_data['creditor_account'] = None
            cleaned_data['creditor_agent'] = None
        else:  # transfer_type == 'creditor'
            if not creditor_account:
                raise ValidationError({
                    'creditor_account': 'La cuenta de acreedor es requerida'
                })
            # Limpiar campo de deudor destino
            cleaned_data['destination_debtor_account'] = None

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        transfer_type = self.cleaned_data.get('transfer_type')
        
        # Generar IDs únicos
        transfer_id = str(uuid.uuid4())
        end_to_end_id = f"E2E{transfer_id[:30]}"
        instruction_id = f"INS{transfer_id[:30]}"
        
        # Preparar datos para el servicio
        data = {
            'payment_id': transfer_id,
            'end_to_end_id': end_to_end_id,
            'instruction_id': instruction_id,
            'debtor_account': instance.debtor_account.iban if instance.debtor_account else None,
            'instructed_amount': instance.instructed_amount,
            'currency': instance.currency or 'EUR',
            'purpose_code': instance.purpose_code or 'GDSV',
            'requested_execution_date': instance.requested_execution_date or timezone.now().date(),
            'remittance_information_unstructured': instance.remittance_information_unstructured,
        }

        if transfer_type == 'debtor':
            destination_account = self.cleaned_data.get('destination_debtor_account')
            data['creditor_account'] = destination_account.iban if destination_account else None
        else:
            data['creditor_account'] = instance.creditor_account.iban if instance.creditor_account else None
            data['creditor_agent'] = instance.creditor_agent

        try:
            transfer = TransferService.create_transfer(data)
            LogTransferencia.objects.create(
                registro=transfer.payment_id,
                tipo_log='TRANSFER',
                contenido=f'Transferencia {"entre deudores" if transfer_type == "debtor" else "a acreedor"} creada: {transfer.payment_id}'
            )
            return transfer
        except ValidationError as e:
            if hasattr(e, 'message_dict'):
                raise
            error_message = str(e)
            if 'débito' in error_message.lower():
                raise ValidationError({'debtor_account': error_message})
            elif 'crédito' in error_message.lower():
                raise ValidationError({'destination_debtor_account' if transfer_type == 'debtor' else 'creditor_account': error_message})
            elif 'saldo' in error_message.lower():
                raise ValidationError({'instructed_amount': error_message})
            else:
                raise ValidationError({'__all__': error_message})
```

