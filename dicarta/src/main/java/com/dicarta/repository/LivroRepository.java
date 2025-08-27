package com.dicarta.repository;


import com.dicarta.model.Livro;
import org.springframework.data.jpa.repository.JpaRepository;


public interface LivroRepository extends JpaRepository<Livro, Long> {}