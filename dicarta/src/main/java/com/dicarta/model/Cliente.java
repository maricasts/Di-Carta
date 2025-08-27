package com.dicarta.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import lombok.Data; // Adicionado Lombok

@Data 
@Entity
@Table(name = "cliente")
public class Cliente {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_cliente")
    private Long id;

    @NotBlank
    @Size(max = 100)
    private String nome;

    @NotBlank
    @Column(unique = true, length = 11)
    private String cpf;

    @Size(max = 15)
    private String telefone;

    @Size(max = 100)
    private String email;

    @Size(max = 8)
    private String cep;

    @Size(max = 150)
    private String endereco;
}
