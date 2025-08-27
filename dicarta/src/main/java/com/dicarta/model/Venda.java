package com.dicarta.model;

import jakarta.persistence.*;
import java.time.LocalDate;
import java.util.List;
import lombok.Data; // Adicionado Lombok

@Data // Adicionado Lombok para getters e setters
@Entity
@Table(name = "venda")
public class Venda {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_venda")
    private Long id;

    @Column(nullable = false)
    private LocalDate data;

    @Column(nullable = false, precision = 10, scale = 2)
    private Double total;

    @ManyToOne
    @JoinColumn(name = "id_funcionario", nullable = false)
    private Funcionario funcionario;

    @ManyToOne
    @JoinColumn(name = "id_cliente", nullable = false)
    private Cliente cliente;

    @OneToMany(mappedBy = "venda", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<ItemVenda> itens;
}