const openPopupBtn = document.getElementById('new-task');
const popup = document.getElementById('Pop-up-modal');
const taskDetailsModal = document.getElementById('Pop-up-task-modal');
const projectDetailModal = document.getElementById('project-display-pop-up-modal');

//New Task Modal

const openProjectBtn = document.getElementById('new-project');
const projectPopUp = document.getElementById('project-pop-up-modal');
//New Project Modal


const closeButtons = document.querySelectorAll('.exit');
const saveProjectBtn = document.getElementById('save-project'); // Solo el botón del formulario de proyectos
const resetForm = document.querySelectorAll('.pop-up-form');
const taskForm = document.querySelector('.pop-up-form[method="POST"]'); // Formulario de tareas

//Project Selection for Task
const projectSelection = document.querySelector('.project-selection');
const projectSelectionPopUp = document.querySelector('.project-selection-pop-up');
const taskHistoryDisplay = document.querySelectorAll('.task-history-link');

// Manejar clicks en los botones de tarea
const taskCardButtons = document.querySelectorAll('.task-card-btn');
let currentTaskId = null; // Variable para guardar el ID de la tarea actual

//Manejar el Histrial del Usuario
const historyPopUp = document.getElementById('history-pop-up');
const historyBtn = document.getElementById('history-btn');

if (historyBtn) {
    historyBtn.addEventListener('click', () => {
        historyPopUp.classList.add('visible');
    });
}



// La variable 'currentProjectId' ahora se define en home.html como 'window.currentProjectId'
// cuando se está en la vista de un proyecto. Ya no necesitamos declararla aquí.

// Función para reiniciar el formulario de tareas a su estado original
function resetTaskForm() {
    const editForm = document.querySelector('#Pop-up-modal .pop-up-form');
    if (editForm) {
        editForm.reset(); // Limpia los campos del formulario
        editForm.action = "/"; // Restaura la acción original para crear tarea

        // Restaura el título y el texto del botón
        const titleElement = document.querySelector('#Pop-up-modal .pop-up-title h1');
        const saveButton = document.querySelector('#Pop-up-modal .save');
        if (titleElement) titleElement.textContent = 'New Task';
        if (saveButton) saveButton.value = 'Save';
    }
}

closeButtons.forEach(button => {
    button.addEventListener('click', () => {
        // Solución Error 1: Verificar si el modal existe antes de manipularlo.
        // Esto evita el error 'Cannot read properties of null' si el modal no está en el DOM.
        if (projectDetailModal) projectDetailModal.classList.remove('visible');
        if (projectPopUp) projectPopUp.classList.remove('visible');
        if (historyPopUp) historyPopUp.classList.remove('visible');
        if (popup) popup.classList.remove('visible');
        if (taskDetailsModal) taskDetailsModal.classList.remove('visible');
        if (projectSelectionPopUp) projectSelectionPopUp.classList.remove('visible');

        // Al cerrar cualquier modal, nos aseguramos de que el form de tareas se reinicie
        resetTaskForm();
    });
});


taskCardButtons.forEach(button => {
    button.addEventListener('click', (e) => {
        // Obtener los datos de la tarea desde los data-attributes
        const taskId = button.getAttribute('data-task-id');
        const taskTitle = button.getAttribute('data-task-title');
        const taskDescription = button.getAttribute('data-task-description');
        const taskDate = button.getAttribute('data-task-date');
        const taskCompleted = button.getAttribute('data-task-completed') === 'True';
        const taskDeadline = button.getAttribute('data-task-deadline');
        
        // Guardar el ID de la tarea actual
        currentTaskId = taskId;
        
        // Llenar el pop-up con los datos
        document.getElementById('task-detail-title').textContent = taskTitle;
        document.getElementById('task-detail-description').textContent = taskDescription;
        document.getElementById('task-detail-date').textContent = 'Created: ' + taskDate;

        // Llenar la fecha límite si existe
        const deadlineElement = document.getElementById('task-detail-deadline');
        if (taskDeadline) {
            deadlineElement.textContent = 'Deadline: ' + taskDeadline;
            deadlineElement.style.display = 'block'; // Asegurarse de que sea visible
        } else {
            deadlineElement.textContent = ''; // Limpiar por si acaso
            deadlineElement.style.display = 'none'; // Ocultar si no hay fecha límite
        }
        
        // Actualizar el estado
        const statusElement = document.getElementById('task-detail-status');
        const completeBtn = document.getElementById('complete-task-btn');
        if (taskCompleted) {
            statusElement.textContent = 'Status: Completed';
            completeBtn.textContent = 'Mark as Incomplete';
            completeBtn.disabled = false;
        } else {
            statusElement.textContent = 'Status: Pending';
            completeBtn.textContent = 'Mark as Complete';
            completeBtn.disabled = false;
        }
        
        // Mostrar el pop-up
        taskDetailsModal.classList.add('visible');
    });
});

// Solución: Usar querySelectorAll para obtener todos los enlaces y recorrerlos.
// Esto evita el error si no hay enlaces y hace que todos funcionen.
taskHistoryDisplay.forEach(link => {
    link.addEventListener('click', (event) => {
        event.preventDefault(); // Prevenir que el enlace '#' recargue la página

        const taskId = link.getAttribute('data-task-id');
        const taskTitle = link.getAttribute('data-task-title');
        const taskDescription = link.getAttribute('data-task-description');
        const taskDate = link.getAttribute('data-task-date');
        const taskCompleted = link.getAttribute('data-task-completed') === 'True';
        const taskDeadline = link.getAttribute('data-task-deadline');
        
        // Guardar el ID de la tarea actual
        currentTaskId = taskId;
        document.getElementById('task-detail-title').textContent = taskTitle;
        document.getElementById('task-detail-description').textContent = taskDescription;
        document.getElementById('task-detail-date').textContent = 'Created: ' + taskDate;

        // Llenar la fecha límite si existe
        const deadlineElement = document.getElementById('task-detail-deadline');
        if (taskDeadline) {
            deadlineElement.textContent = 'Deadline: ' + taskDeadline;
            deadlineElement.style.display = 'block';
        } else {
            deadlineElement.style.display = 'none';
        }
        
        // Actualizar el estado
        const statusElement = document.getElementById('task-detail-status');
        const completeBtn = document.getElementById('complete-task-btn');
        if (taskCompleted) {
            statusElement.textContent = 'Status: Completed';
            completeBtn.textContent = 'Mark as Incomplete';
        } else {
            statusElement.textContent = 'Status: Pending';
            completeBtn.textContent = 'Mark as Complete';
        }
        
        // Mostrar el pop-up
        taskDetailsModal.classList.add('visible');
    });
});

projectSelection.addEventListener('click', () => {
    projectSelectionPopUp.classList.add('visible');
});

openPopupBtn.addEventListener('click', () => {
    popup.classList.add('visible'); // Show the popup
});

openProjectBtn.addEventListener('click', () => {
    projectPopUp.classList.add('visible'); // Show the popup
});

// El segundo listener de 'closeButtons' ha sido eliminado porque era redundante.
// La lógica de reseteo de formularios se ha mejorado y movido a la función 'resetTaskForm'
// y se llama desde el primer listener de 'closeButtons'.


// Cerrar el pop-up de detalles de tarea
const closeTaskDetailsBtn = document.getElementById('close-task-details'); // Para el modal de tareas
const closeProjectDetailsBtn = document.getElementById('close-project-details'); // Para el modal de proyectos

if (closeTaskDetailsBtn) {
    closeTaskDetailsBtn.addEventListener('click', () => {
        taskDetailsModal.classList.remove('visible');
         // Cierra el modal de tareas
    });
}




// Manejar el botón submit del formulario de tareas
const saveTaskBtn = document.getElementById('save');
if (saveTaskBtn && taskForm) {
    saveTaskBtn.addEventListener('click', (e) => {
        // Cerrar el popup cuando se hace clic en Save
        // No prevenimos el envío del formulario, solo ocultamos el modal.
        // El formulario se enviará de forma nativa.
        // NOTA: El formulario se reiniciará la próxima vez que se cierre un modal.
        popup.classList.remove('visible');
        projectSelectionPopUp.classList.remove('visible');
        
        // El formulario se enviará normalmente después de esto
    });
}

// Manejar solo el botón de guardar del formulario de proyectos
if (saveProjectBtn) {
    saveProjectBtn.addEventListener('click', (e) => {
        e.preventDefault(); // Prevenir el comportamiento por defecto
        projectPopUp.classList.remove('visible');
        popup.classList.remove('visible');
        projectSelectionPopUp.classList.remove('visible');

        resetForm.forEach(form => {
            form.reset();
        })
    });
}

// Botón de completar tarea
const completeTaskBtn = document.getElementById('complete-task-btn');
if (completeTaskBtn) {
    completeTaskBtn.addEventListener('click', () => {
        if (currentTaskId) {
            // Crear un formulario para enviar la petición
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `/task/${currentTaskId}/complete`;
            
            // Agregar CSRF token si es necesario (Flask-WTF)
            const csrfToken = document.querySelector('input[name="csrf_token"]');
            if (csrfToken) {
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrf_token';
                csrfInput.value = csrfToken.value;
                form.appendChild(csrfInput);
            }
            
            document.body.appendChild(form);
            form.submit();
        }
    });
}

// Botón de eliminar tarea
const deleteTaskBtn = document.getElementById('delete-task-btn');
if (deleteTaskBtn) {
    deleteTaskBtn.addEventListener('click', () => {
        if (currentTaskId) { // Eliminamos la confirmación del navegador
            // Crear un formulario para enviar la petición
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `/task/${currentTaskId}/delete`;
            
            // Agregar CSRF token si es necesario (Flask-WTF)
            const csrfToken = document.querySelector('input[name="csrf_token"]');
            if (csrfToken) {
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrf_token';
                csrfInput.value = csrfToken.value;
                form.appendChild(csrfInput);
            }
            
            document.body.appendChild(form);
            form.submit();
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert, .alert-success, .alert-warning, .alert-danger, .alert-info');
    alerts.forEach(el => {
      // Después de 3 segundos, iniciar la animación de salida
      setTimeout(() => {
        el.classList.add('alert-dismiss');
        // Remover del DOM después de que termine la animación (0.4s)
        setTimeout(() => el.remove(), 400);
      }, 3000); // 3s visible
    });
  });

  // Manejar clics en los nuevos botones de completar de la lista
const completeTaskListBtns = document.querySelectorAll('.complete-task-list-btn');

completeTaskListBtns.forEach(button => {
    button.addEventListener('click', (event) => {
        // Detenemos la propagación para no activar otros clics (si los hubiera)
        event.stopPropagation(); 

        const taskId = button.getAttribute('data-task-id');

        if (taskId) {
            // Creamos un formulario dinámicamente para enviar la petición POST
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `/task/${taskId}/complete`; // La misma ruta que ya usas

            // Es crucial añadir el token CSRF para la seguridad
            const csrfToken = document.querySelector('input[name="csrf_token"]');
            if (csrfToken) {
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrf_token';
                csrfInput.value = csrfToken.value;
                form.appendChild(csrfInput);
            }

            // Añadimos el formulario al body, lo enviamos y luego lo eliminamos
            document.body.appendChild(form);
            form.submit();
        }

        
    });
});

const projectItems = document.querySelectorAll('.project-item');
const assignProjectBtn = document.querySelector('.project-selection p')
const taskProjectSelect = document.querySelector('select[name="project"]');

projectItems.forEach(item => {
    item.addEventListener('click', () => {
        const selectedProjectId = item.getAttribute('data-project-id');
        const selectedProjectName = item.getAttribute('data-project-name');
        
        if (selectedProjectId) {
            assignProjectBtn.textContent = selectedProjectName;
        } else {
            assignProjectBtn.textContent = 'Assign Project';
        
        }
        
        if (taskProjectSelect) {
            taskProjectSelect.value = selectedProjectId;
        }
        
        projectSelectionPopUp.classList.remove('visible');
    
        
    });

})

const projectDisplayPopUps = document.getElementById('project-name-link');
const projectDisplay = document.getElementById('project-display-pop-up-modal');
const displayProjectHistory = document.getElementById('display-project-history');

if (displayProjectHistory) {
    displayProjectHistory.addEventListener('click',() => {
        projectDisplay.classList.add('visible');
    })
}


if (projectDisplayPopUps) { // Añadimos esta comprobación
    projectDisplayPopUps.addEventListener('click', () => {
        projectDisplay.classList.add('visible');
    });
}

const completeProjectBtn = document.getElementById('complete-project-btn');
if (completeProjectBtn) {
    completeProjectBtn.addEventListener('click', () => {
        if (window.currentProjectId) { // PASO 2: Usamos la variable global que creamos
            // Crear un formulario para enviar la petición
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = `/project/${window.currentProjectId}/complete`; // Usamos la variable global aquí también
            
            // Agregar CSRF token si es necesario (Flask-WTF)
            const csrfToken = document.querySelector('input[name="csrf_token"]');
            if (csrfToken) {
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrf_token';
                csrfInput.value = csrfToken.value;
                form.appendChild(csrfInput);
            }
            
            document.body.appendChild(form);
            form.submit();
        }
    });
}

// Botón para editar tarea (dentro del modal de detalles)
const editTaskBtn = document.getElementById('edit');
if (editTaskBtn) {
    editTaskBtn.addEventListener('click', () => {
        if (currentTaskId) {
            // 1. Ocultar el modal de detalles de la tarea
            taskDetailsModal.classList.remove('visible');

            // 2. Obtener los datos de la tarea actual desde el modal de detalles
            const taskTitle = document.getElementById('task-detail-title').textContent;
            const taskDescription = document.getElementById('task-detail-description').textContent;
            // Para la fecha, necesitamos el formato YYYY-MM-DD que usa el input[type=date]
            // Asumimos que el data-attribute del enlace original tiene este formato.
            const originalLink = document.querySelector(`.task-card-btn[data-task-id="${currentTaskId}"], .task-history-link[data-task-id="${currentTaskId}"]`);
            const taskDeadline = originalLink ? originalLink.getAttribute('data-task-deadline') : '';

            // 3. Poblar el formulario de edición (que es el mismo que el de nueva tarea)
            const editForm = document.querySelector('#Pop-up-modal .pop-up-form');
            const editFormTitle = editForm.querySelector('.task-name');
            const editFormDescription = editForm.querySelector('.task-details');
            const editFormDeadline = editForm.querySelector('.task-deadline');

            editFormTitle.value = taskTitle;
            editFormDescription.value = taskDescription;
            editFormDeadline.value = taskDeadline;

            // 4. Cambiar la acción del formulario para que apunte a la ruta de edición
            editForm.action = `/task/${currentTaskId}/edit`;

            // 5. Cambiar el título del pop-up y el texto del botón
            document.querySelector('#Pop-up-modal .pop-up-title h1').textContent = 'Edit Task';
            document.querySelector('#Pop-up-modal .save').value = 'Update';

            // 6. Mostrar el pop-up de edición
            popup.classList.add('visible');
        }
    });
}
/*
const opentaskPopUpMobile = document.getElementById('new-task-mobile');
const openProjectPopUpMobile = document.getElementById('new-project-mobile');

opentaskPopUpMobile.addEventListener('click', () =>{
    popup.classList.add('visible');
})

openProjectPopUpMobile.addEventListener('click', () =>{
    projectPopUp.classList.add('visible');
})
*/
const openMenuBtn = document.getElementById('open-menu');
const closeMenuBtn = document.getElementById('close-menu');
const menu = document.getElementById('menu');

openMenuBtn.addEventListener('click', () => {
    menu.classList.add('show');
    openMenuBtn.classList.toggle('spin');
    });

closeMenuBtn.addEventListener('click', () => {
    menu.classList.remove('show');
    closeMenuBtn.classList.toggle('spin-again');
    });
/*
const openMobileSelection = document.getElementById('mobile-project-block');
const closeMobileSelection = document.getElementById('close-project-block');
const projectAndTaskselection = document.getElementById('mobile-projects-task');

openMobileSelection.addEventListener('click',() => {
    projectAndTaskselection.classList.add('visible-mobile');
})

closeMobileSelection.addEventListener('click', () =>{
    projectAndTaskselection.classList.remove('visible-mobile')
}) */