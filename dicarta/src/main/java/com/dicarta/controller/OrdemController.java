package com.dicarta.controller;

import com.dicarta.model.OrdemDeServico;
import com.dicarta.service.OrdemService;
import com.dicarta.service.custos.CustoPorHora; // Importar a classe de custo
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@RestController
@RequestMapping("/ordens")
public class OrdemController {

    private final OrdemService ordemService;

    public OrdemController(OrdemService ordemService) {
        this.ordemService = ordemService;
        // Exemplo de como registrar um observer e definir uma estratégia de custo
        // Isso pode ser feito em um @PostConstruct ou em uma classe de configuração
        ordemService.registrarObserver(new com.dicarta.observer.LoggerObserver());
        ordemService.setCalculoCusto(new CustoPorHora(50.0)); // Exemplo: R$50 por hora
    }

    @PostMapping
    public ResponseEntity<OrdemDeServico> criarOrdem(@RequestBody OrdemDeServico ordemDeServico) {
        OrdemDeServico novaOrdem = ordemService.salvar(ordemDeServico);
        return new ResponseEntity<>(novaOrdem, HttpStatus.CREATED);
    }

    @GetMapping
    public ResponseEntity<List<OrdemDeServico>> listarOrdens() {
        List<OrdemDeServico> ordens = ordemService.listar();
        return new ResponseEntity<>(ordens, HttpStatus.OK);
    }

    @GetMapping("/{id}")
    public ResponseEntity<OrdemDeServico> buscarOrdemPorId(@PathVariable Long id) {
        Optional<OrdemDeServico> ordem = ordemService.findById(id);
        return ordem.map(value -> new ResponseEntity<>(value, HttpStatus.OK))
                .orElseGet(() -> new ResponseEntity<>(HttpStatus.NOT_FOUND));
    }

    @PutMapping("/{id}/status")
    public ResponseEntity<OrdemDeServico> atualizarStatusOrdem(@PathVariable Long id, @RequestParam String novoStatus) {
        try {
            OrdemDeServico updatedOs = ordemService.atualizarStatus(id, novoStatus);
            return new ResponseEntity<>(updatedOs, HttpStatus.OK);
        } catch (RuntimeException e) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }

    @GetMapping("/{id}/custo")
    public ResponseEntity<Double> calcularCustoOrdem(@PathVariable Long id) {
        Optional<OrdemDeServico> ordem = ordemService.findById(id);
        if (ordem.isPresent()) {
            try {
                double custo = ordemService.calcularCusto(ordem.get());
                return new ResponseEntity<>(custo, HttpStatus.OK);
            } catch (IllegalStateException e) {
                return new ResponseEntity<>(HttpStatus.INTERNAL_SERVER_ERROR); // Ou outro status apropriado
            }
        } else {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }
    }
}