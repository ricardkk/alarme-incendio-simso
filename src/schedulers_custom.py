"""Deadline Monotonic como política do SimSo; o motor permanece inalterado."""

from simso.core import Scheduler


class DM(Scheduler):
    """Prioridade fixa pelo deadline relativo; empates pelo identificador."""

    def init(self):
        """Inicializa a fila de jobs ativados pelo motor."""
        if len(self.processors) != 1:
            raise ValueError("Esta política DM implementa apenas uma CPU.")
        self.ready_list = []

    def on_activate(self, job):
        """Solicita uma decisão após a liberação de um job."""
        self.ready_list.append(job)
        job.cpu.resched()

    def on_terminated(self, job):
        """Remove o job concluído ou abortado e reavalia a CPU."""
        if job in self.ready_list:
            self.ready_list.remove(job)
        job.cpu.resched()

    def schedule(self, cpu):
        """Entrega ao SimSo o job ativo com maior prioridade."""
        active_jobs = [job for job in self.ready_list if job.is_active()]
        job = min(active_jobs, key=lambda item: (
            item.deadline, item.task.identifier, item.activation_date), default=None)
        return (job, cpu)
