document.addEventListener('htmx:afterSwap', (event) => {
  if (event.detail.target.id === 'player-table-body') {
    attachTeamAssignmentHandlers();
  }
});

document.addEventListener('DOMContentLoaded', () => {
  attachTeamAssignmentHandlers();
});

function attachTeamAssignmentHandlers() {
  document.querySelectorAll('[data-assignment-form]').forEach((trigger) => {
    trigger.removeEventListener('click', openAssignmentForm);
    trigger.addEventListener('click', openAssignmentForm);
  });
}

async function openAssignmentForm(event) {
  event.preventDefault();
  const button = event.currentTarget;
  const url = button.dataset.assignmentForm;
  const row = button.closest('tr');
  if (!row) return;

  const response = await fetch(url, {
    headers: {
      'HX-Request': 'true',
    },
  });

  if (!response.ok) {
    console.error('Failed to load assignment form');
    return;
  }

  const modalContainer = document.getElementById('teamAssignmentModal');
  modalContainer.innerHTML = await response.text();
  const modal = new bootstrap.Modal(document.getElementById('teamAssignmentModalDialog'));
  modal.show();
}
