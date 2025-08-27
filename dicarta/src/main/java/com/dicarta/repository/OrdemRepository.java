package com.dicarta.repository;


import com.dicarta.model.OrdemDeServico;
import org.springframework.data.jpa.repository.JpaRepository;


public interface OrdemRepository extends JpaRepository<OrdemDeServico, Long> {}