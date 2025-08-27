package com.dicarta.model;

import jakarta.persistence.*;
import lombok.Data; // Adicionado Lombok

@Data // Adicionado Lombok para getters e setters
@Entity
@Table(name = "itemvenda")
public class ItemVenda {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "id_item")
    private Long id;

    @ManyToOne
    @JoinColumn(name = "id_venda", nullable = false)
    private Venda venda;

    @ManyToOne
    @JoinColumn(name = "id_livro", nullable = false)
    private Livro livro;

    @Column(nullable = false)
    private Integer quantidade;

    @Column(name = "preco_unitario", nullable = false, precision = 10, scale = 2)
    private Double precoUnitario;
}