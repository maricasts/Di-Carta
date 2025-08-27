package com.dicarta.observer;


import com.dicarta.model.OrdemDeServico;


public interface OrdemStatusObserver {
void statusAlterado(OrdemDeServico os, String antigo, String novo);
}