/**
 * CARF Keycloak Login Theme - JavaScript
 * Sistema de Regularização Fundiária Urbana
 *
 * Funcionalidades:
 * - Toggle de visibilidade de senha (olhinho)
 * - Acessibilidade (ARIA attributes)
 */

(function() {
  'use strict';

  document.addEventListener('DOMContentLoaded', function() {
    initPasswordToggles();
    improveFormAccessibility();
  });

  /**
   * Inicializa toggles de visibilidade de senha (olhinho)
   */
  function initPasswordToggles() {
    var toggles = document.querySelectorAll('.password-toggle');
    toggles.forEach(function(btn) {
      btn.addEventListener('click', function() {
        var wrapper = btn.closest('.password-wrapper');
        var input = wrapper.querySelector('input');
        var eyeIcon = btn.querySelector('.eye-icon');
        var eyeOffIcon = btn.querySelector('.eye-off-icon');

        if (input.type === 'password') {
          input.type = 'text';
          eyeIcon.style.display = 'none';
          eyeOffIcon.style.display = 'block';
          btn.setAttribute('aria-label', 'Ocultar senha');
        } else {
          input.type = 'password';
          eyeIcon.style.display = 'block';
          eyeOffIcon.style.display = 'none';
          btn.setAttribute('aria-label', 'Mostrar senha');
        }
      });
    });
  }

  /**
   * Melhora acessibilidade do formulário
   */
  function improveFormAccessibility() {
    var form = document.getElementById('kc-form-login');
    if (form && !form.getAttribute('role')) {
      form.setAttribute('role', 'form');
    }
  }

})();
