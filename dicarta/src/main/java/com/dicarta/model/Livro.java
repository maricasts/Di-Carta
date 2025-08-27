package com.dicarta.model;

import jakarta.persistence.*;
import lombok.Data; // Adicionado Lombok

@Data
@Entity
@Table(name = "livro")
public class Livro {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_livro")
    private Long id;

    private String titulo;
    private String autor;
    private String editora;
    private Integer ano;
    private String genero;

    @Column(precision = 10, scale = 2)
    private Double preco;

    @Column(columnDefinition = "integer default 0")
    private Integer estoque;
}