package com.dicarta.model;

import jakarta.persistence.*;
import lombok.Data; // Adicionado Lombok

@Data // Adicionado Lombok para getters e setters
@Entity
public class OrdemDeServico {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private String cliente;
    private String tipo; // Preventiva, Corretiva
    private String status; // Aberta, Em Andamento, Fechada
    private int horas;
}