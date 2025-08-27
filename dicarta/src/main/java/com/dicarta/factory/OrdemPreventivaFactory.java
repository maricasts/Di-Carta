package com.dicarta.factory;


import com.dicarta.model.OrdemDeServico;


public class OrdemPreventivaFactory extends OrdemFactory {
@Override
public OrdemDeServico criar(String cliente) {
OrdemDeServico os = new OrdemDeServico();
os.setCliente(cliente);
os.setTipo("Preventiva");
os.setStatus("Aberta");
return os;
}
}