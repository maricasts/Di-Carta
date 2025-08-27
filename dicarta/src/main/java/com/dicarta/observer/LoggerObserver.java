package com.dicarta.observer;


import com.dicarta.model.OrdemDeServico;


public class LoggerObserver implements OrdemStatusObserver {
@Override
public void statusAlterado(OrdemDeServico os, String antigo, String novo) {
System.out.println("Ordem " + os.getId() + " mudou de status de " + antigo + " para " + novo);
}
}