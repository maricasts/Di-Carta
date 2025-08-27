package com.dicarta.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import lombok.Data; // Adicionado Lombok

@Data 
@Entity
@Table(name = "funcionario")
public class Funcionario {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_funcionario")
    private Long id;

    @NotBlank
    @Size(max = 100)
    private String nome;

    @NotBlank
    @Column(unique = true, length = 11)
    private String cpf;

    @NotBlank
    @Size(max = 20)
    private String status; // Contratado, Demitido

    @Column(name = "valor_hora", precision = 10, scale = 2)
    private Double valorHora;

    @Column(name = "carga_horaria")
    private Integer cargaHoraria;
}
