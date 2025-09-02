package com.dicarta.livraria.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import java.util.List;
import java.time.LocalDate;
import com.dicarta.livraria.model.OrdemDeServico;
import com.dicarta.livraria.repository.OrdemDeServicoRepository;

@RestController
@RequestMapping("/api/os")
public class OrdemDeServicoController {
    private final OrdemDeServicoRepository repo;
    public OrdemDeServicoController(OrdemDeServicoRepository repo) { this.repo = repo; }

    @GetMapping
    public List<OrdemDeServico> all() { return repo.findAll(); }

    @PostMapping
    public ResponseEntity<OrdemDeServico> create(@RequestBody OrdemDeServico os) {
        os.setDataAbertura(LocalDate.now());
        if (os.getStatus() == null) os.setStatus("ABERTA");
        OrdemDeServico saved = repo.save(os);
        return ResponseEntity.ok(saved);
    }

    @GetMapping("/{id}")
    public ResponseEntity<OrdemDeServico> get(@PathVariable Long id) {
        return repo.findById(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PutMapping("/{id}")
    public ResponseEntity<OrdemDeServico> update(@PathVariable Long id, @RequestBody OrdemDeServico os) {
        return repo.findById(id).map(existing -> {
            existing.setDescricao(os.getDescricao());
            existing.setStatus(os.getStatus());
            existing.setDataFechamento(os.getDataFechamento());
            repo.save(existing);
            return ResponseEntity.ok(existing);
        }).orElse(ResponseEntity.notFound().build());
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        if (!repo.existsById(id)) return ResponseEntity.notFound().build();
        repo.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
