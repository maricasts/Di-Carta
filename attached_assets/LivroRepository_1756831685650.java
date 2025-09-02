package com.dicarta.livraria.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import com.dicarta.livraria.model.Livro;

@Repository
public interface LivroRepository extends JpaRepository<Livro, Long> {
}
