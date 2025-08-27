package com.dicarta.factory;

import com.dicarta.model.OrdemDeServico;

public abstract class OrdemFactory {
    public abstract OrdemDeServico criar(String cliente);
}