
document.addEventListener("DOMContentLoaded", function() {
    //enviar el form
    const form = document.querySelector("#msform");
    form.addEventListener("submit", (e) => {
        e.preventDefault(); 
        const formData = new FormData(form);
        fetch('submitForm/', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }
            return response.json(); 
        })
        .then(data => {
            console.log(data.success)
            
            // try {
                // const jsonData = JSON.parse(data);
                if (data.success) {
                    showModal(data.mensaje);
                    // setTimeout(() => {
                    //     window.location.href = 'asociarme/';
                    // }, 2000); 
                    
                } else {
                    alert('Error al guardar el socio');
                }
            // } catch (e) {
            //     console.error('Error al parsear JSON:', e);
            // }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Hubo un problema al enviar el formulario.');
        });
    
    });
    function showModal(message) {
        const modal = document.getElementById("modal");
        const modalText = modal.querySelector("#modal-text"); 
        if (modalText) {
            modalText.textContent = message;
        }
        modal.style.display = "block";
    
        const closeButton = modal.querySelector(".close-btn");
        closeButton.addEventListener("click", () => {
            modal.style.display = "none";
            window.location.href = '/asociarme';
        });
        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
                window.location.href = '/asociarme';
            }
        };
    }
    
    //validaciones y cambiar de pasos en el form
    const nextButtons = document.querySelectorAll(".next");
    const previousButtons = document.querySelectorAll(".previous");
    const fieldsets = document.querySelectorAll("#msform div.fieldset-group");
    const progressItems = document.querySelectorAll("#progressbar li");
    let currentStep = 1; 
    nextButtons.forEach((button) => {
        button.addEventListener("click", async () => {
            if (validateStep()) {
                let valid = true;

                if (currentStep === 2) { 
                    const dniValid = await validateDni();
                    const cuilValid = await validateCuil();
                    valid = dniValid && cuilValid;
                    const emailValid = await validateEmail();
                    const useEmail = validateUseEmail();
                    valid = emailValid && useEmail;
                }

                if (valid) {
                    clearErrors();
                    changeStep(1); 
                } 
            } else {
                showGlobalErrorMessage();
            }
        });
    });

    previousButtons.forEach((button) => {
        button.addEventListener("click", () => {
            clearErrors();
            changeStep(-1);
        });
    });
    const inputs = document.querySelectorAll("input, select, textarea");
    inputs.forEach((input) => {
        input.addEventListener("input", () => {
            if (input.value) {
                input.classList.remove("invalid");
            }
        });
    });
    function validateStep() {
        const currentFieldset = document.querySelector("#msform div.fieldset-group.active");
        const inputs = currentFieldset.querySelectorAll("input, select, textarea");
        let isValid = true;

        inputs.forEach((input) => {
            // Eliminar cualquier clase de error anterior
            input.classList.remove("invalid");
            
            // Verificar si el campo es requerido y está vacío
            if (input.required && !input.value) {
                input.classList.add("invalid");
                isValid = false;
            }
            
        });
        validateDni();
        validateCuil();

        return isValid;
    }

    async function validateDni(){
        const dni = document.getElementById("nro_doc").value;

        try {
            const response = await fetch(`verificar_dni/${dni}/`);
            const data = await response.json();
            
            if (data.registrado) {
                const errorLabel = document.querySelector(".form-group #nro_doc + .form-label-error");
                errorLabel.innerText = "El DNI ya se encuentra registrado.";
                return false;
            }
    
            return true;  
        } catch (error) {
            console.error("Error al verificar el DNI:", error);
            return false;  
        }
    }

    async function validateCuil(){
        const CUIL = document.getElementById("CUIL").value;

        try {
            const response = await fetch(`/verificar_cuil/${CUIL}/`);
            const data = await response.json();
            
            if (data.invalido || data.registrado) {
                const errorLabel = document.querySelector(".form-group #CUIL + .form-label-error");
                errorLabel.innerText = data.invalido ? "El CUIL ingresado es inválido" : "El CUIL ya se encuentra registrado.";
                return false;  
            }

            return true;  
        } catch (error) {
            console.error("Error al verificar el CUIL:", error);
            return false;  
        }
    }
    async function validateEmail(){
        const email = document.getElementById("email").value.trim();
        if (!email) {
            return true;
        }
        try {
            const response = await fetch(`verificar_email/${email}/`);
            const data = await response.json();
            console.log(data.registrado)
            if (data.registrado) {
                const errorLabel = document.querySelector(".form-group #email + .form-label-error");
                errorLabel.innerText = "El email ya se encuentra registrado.";
                return false;
            }
    
            return true;  
        } catch (error) {
            console.error("Error al verificar el email:", error);
            return false;  
        }
    }
    function validateUseEmail(){
        const use_email = document.getElementById("usa_email").value;
        if (use_email == 1){
            const email = document.getElementById("email").value;
            if (!email){
                const errorLabel = document.querySelector(".form-group #usa_email + .form-label-error");
                errorLabel.innerText = `Si selecciona que "Sí" debe indicar un email`;
                return false;
            } else {
                return true;
            }
        }
        return true;
    }
  
   

    function showGlobalErrorMessage() {
        // Eliminar cualquier mensaje global anterior
        const existingMessage = document.querySelector(".global-error-message");
        if (existingMessage) {
            existingMessage.remove();
        }

        const currentFieldset = document.querySelector("#msform div.fieldset-group.active");

        // Crear el mensaje de error global
        const errorMessage = document.createElement("div");
        errorMessage.classList.add("global-error-message");
        errorMessage.style.color = "red"; 
        errorMessage.textContent = "Por favor, complete todos los campos requeridos.";

        // Insertar el mensaje al final del paso
        currentFieldset.appendChild(errorMessage);
    }
    function clearErrors() {
        const currentFieldset = document.querySelector("#msform div.fieldset-group.active");
        const inputs = currentFieldset.querySelectorAll("input, select, textarea");

        inputs.forEach((input) => {
            input.classList.remove("invalid");
            const errorLabels = input.parentNode.querySelectorAll(".form-label-error");
            errorLabels.forEach(label => label.textContent="");
        });

        const existingMessage = document.querySelector(".global-error-message");
        if (existingMessage) {
            existingMessage.remove();
        }
    }
    function changeStep(direction) {
        const currentFieldset = document.querySelector("#msform div.fieldset-group.active");
        let currentIndex = Array.from(fieldsets).indexOf(currentFieldset);

        let nextIndex = currentIndex + direction;
        if (nextIndex < 0 || nextIndex >= fieldsets.length) return;

        // Actualizar el paso actual
        currentFieldset.classList.remove("active");
        fieldsets[nextIndex].classList.add("active");
        
        //scrollear arriba hasta el titulo
        const title = document.getElementById("title-asociarme");
        if (title) {
            title.scrollIntoView({ behavior: "smooth", block: "start" });
        }
        
        // Actualizar el progreso
        if (direction === 1) {
            progressItems[nextIndex].classList.add("ver");
            progressItems[nextIndex].classList.add("active");
        } else if (direction === -1) {
            progressItems[currentIndex].classList.remove("ver");
            progressItems[currentIndex].classList.remove("active");
        }
        // const firstInput = fieldsets[newIndex].querySelector("input, select, textarea");
        // if (firstInput) {
        //     firstInput.focus();
        // }
        currentStep += direction;

    }
});


            // if (input.name === "fecha_nac" && input.value) {
            //     const today = new Date();
            //     const fechaNac = new Date(input.value);
            //     console.log(today, fechaNac)
            //     if (fechaNac > today) {
            //         input.classList.add("invalid");

            //         // Encontrar el label de error asociado con el input
            //         const errorLabel = input.parentNode.querySelector(".form-label-error");
            //         if (errorLabel) {
            //             errorLabel.textContent = "La fecha de nacimiento no puede ser mayor al día de hoy.";
            //         }

            //         isValid = false;
            //     }
            // }