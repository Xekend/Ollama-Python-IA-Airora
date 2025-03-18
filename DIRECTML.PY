import onnxruntime as ort

# Listar los proveedores disponibles
providers = ort.get_available_providers()
print(providers)  # Debería incluir "DML" (DirectML)