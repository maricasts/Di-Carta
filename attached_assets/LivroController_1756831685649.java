package com.dicarta.livraria.controller;

import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;
import java.util.List;
import com.dicarta.livraria.model.Livro;
import com.dicarta.livraria.repository.LivroRepository;

@RestController
@RequestMapping("/api/livros")
public class LivroController {
    private final LivroRepository repo;
    public LivroController(LivroRepository repo) { this.repo = repo; }

    @GetMapping
    public List<Livro> all() { return repo.findAll(); }

    @PostMapping
    public ResponseEntity<Livro> create(@RequestBody Livro l) {
        Livro saved = repo.save(l);
        return ResponseEntity.ok(saved);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Livro> get(@PathVariable Long id) {
        return repo.findById(id).map(ResponseEntity::ok).orElse(ResponseEntity.notFound().build());
    }

    @PutMapping("/{id}")
    public ResponseEntity<Livro> update(@PathVariable Long id, @RequestBody Livro l) {
        return repo.findById(id).map(existing -> {
            existing.setTitulo(l.getTitulo());
            existing.setAutor(l.getAutor());
            existing.setEditora(l.getEditora());
            existing.setAno(l.getAno());
            existing.setGenero(l.getGenero());
            existing.setPreco(l.getPreco());
            existing.setEstoque(l.getEstoque());
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
