package com.dicarta.service.custos;


import com.dicarta.model.OrdemDeServico;


public class CustoPorHora implements CalculoCusto {
private final double valorHora;
public CustoPorHora(double valorHora) { this.valorHora = valorHora; }


@Override
public double calcular(OrdemDeServico os) {
return os.getHoras() * valorHora;
}
}