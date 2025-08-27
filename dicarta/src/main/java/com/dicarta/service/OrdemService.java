    package com.dicarta.service;

    import com.dicarta.model.OrdemDeServico;
    import com.dicarta.observer.OrdemStatusObserver;
    import com.dicarta.repository.OrdemRepository;
    import com.dicarta.service.custos.CalculoCusto;
    import org.springframework.stereotype.Service;

    import java.util.ArrayList;
    import java.util.List;
    import java.util.Optional;

    @Service
    public class OrdemService {
        private final OrdemRepository repo;
        private final List<OrdemStatusObserver> observers = new ArrayList<>();
        private CalculoCusto calculoCusto;

        public OrdemService(OrdemRepository repo) {
            this.repo = repo;
        }

        public OrdemDeServico salvar(OrdemDeServico os) { return repo.save(os); }

        public List<OrdemDeServico> listar() { return repo.findAll(); }

        public Optional<OrdemDeServico> findById(Long id) { return repo.findById(id); }

        public void registrarObserver(OrdemStatusObserver o) { observers.add(o); }

        public void setCalculoCusto(CalculoCusto calculoCusto) { this.calculoCusto = calculoCusto; }

        public double calcularCusto(OrdemDeServico os) {
            if (calculoCusto == null) throw new IllegalStateException("Strategy não configurada");
            return calculoCusto.calcular(os);
        }

        public OrdemDeServico atualizarStatus(Long id, String novoStatus) {
            OrdemDeServico os = repo.findById(id).orElseThrow(() -> new RuntimeException("Ordem de Serviço não encontrada com ID: " + id));
            String antigoStatus = os.getStatus();
            os.setStatus(novoStatus);
            OrdemDeServico updatedOs = repo.save(os);

            // Notificar observadores
            for (OrdemStatusObserver observer : observers) {
                observer.statusAlterado(updatedOs, antigoStatus, novoStatus);
            }
            return updatedOs;
        }
    }
    