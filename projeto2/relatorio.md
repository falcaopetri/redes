# Projeto 2

Obs.: Esse arquivo é na verdade uma cópia do arquivo README.md

## Grupo
<p>Antonio Carlos Falcão Petri</p>
<p>José Antônio dos Santos Júnior</p>

## Descricao
<p>O desafio do laboratorio e criar as topologias em mininet e fazer a configuracao do software quagga 
(ver laboratório de Segurança BGP na última aula).</p>
<p></p>
<p>No final, tratar tudo como um script de topologia e gerar automaticamente as saidas dos comandos.</p>

## Labs:
- Lab1: Configuração Básica de Roteadores Cisco
- Lab2: Configuração de Roteamento Estático
- Lab3: Configuração de Roteamento Dinâmico

<p>Todos os laboratórios já possuem solução para o software ***PacketTracer***, mas queremos em Mininet</p>
<p></p>
<p>Download do PacketTracer e SOLUCOES: http://labcisco.blogspot.com.br/p/laboratorios.html</p>

##Lab 1:
<p>No laboratório 1 foi desenvolvida a topologia expressa pela imagem a seguir:</p>

![alt tag] (https://github.com/falcaopetri/redes/blob/master/projeto2/lab1/res/lab1.png)

<p>Para o desenvolvimento do lab 1, tudo se deu basicamente pela modelagem da topologia para o mininet. Para isso foram adicionados dois hosts e um switch que se ligava aos dois hosts e a um roteador. Como o roteador em questão não se ligava a nada, nos limitamos a utilizar a classe LinuxRouter, que em termos gerais transforma um node em um rodeador por meio do roteamento Linux por Ip Fowarding.</p>
<p>Dessa forma temos todos os elementos da topologia sendo alcançados entre si.</p>
<p>Todo o processo descrito pode ser visto no arquivo "lab1.py" disponivel em: https://github.com/falcaopetri/redes/blob/master/projeto2/lab1/lab1.py</p>


##Lab 2:
<p>No laboratório 2 foi desenvolvida a topologia expressa pela imagem a seguir:</p>

![alt tag] (https://github.com/falcaopetri/redes/blob/master/projeto2/lab2/res/lab2.png)

<p>Para o desenvolvimento do lab 2, o desenvolvimento se deu em partes. Primeiro foi feita a modelagem da topologia de maneira semelhante ao feito no lab1. Porém nesse laboratório precisamos que os roteadores sejam funcionais. Sendo assim adicionamos as instâncias de roteadores a topologia, porém ainda não funcionais. A segunda parte se deu no processo de configuração desses roteadores, para isso foram criados um arquivo de configuração zebra e um bgp para cada roteador. No arquivo Zebra definimos a interface de seus links enquanto no arquivo BGP definimos a "vizinhança" de cada roteador. No caso como só tinhamos dois roteadores a "vizinhança" era delimitada entre os dois. Por fim, foi implementado o código para iniciar os roteadores com as configurações especificadas.</p>
<p>Dessa forma obtivemos todos os elementos da topologia alcançaveis entre si.</p>
<p>O processo de modelagem da topologia pode ser visto no arquivo "lab2.py" disponível em: https://github.com/falcaopetri/redes/blob/master/projeto2/lab2/lab2.py</p>
<p>O processo de configuração dos roteadores por Zebra e BGP (um arquivo de configuração de cada um dos tipos para cada roteador, totalizando quatro arquivos no caso) pode ser visto no diretório "conf" disponível em: https://github.com/falcaopetri/redes/tree/master/projeto2/lab2/conf</p>
<p>O processo de inicialização dos roteadores com as configurações especificadas pode ser visto no arquivo "util.py" disponível em: https://github.com/falcaopetri/redes/blob/master/projeto2/lab2/util.py</p>


##Lab 3:
<p>No laboratório 3 foi desenvolvida a topologia expressa pela imagem a seguir:</p>

![alt tag] (https://github.com/falcaopetri/redes/blob/master/projeto2/lab3/res/lab3.png)

<p>O desenvolvimento do lab3, mais uma vez se deu de maneira quase que sequencial ao lab2. Todo o processo utilizado no lab2 foi feito também para a topologia em questão, desde a modelagem da topologia para mininet até a inicialização dos roteadores com as configurações determinadas pelos arquivos Zebra e BGP. A única diferença em todo o processo até então é que como nesta topologia temos três roteadores a vizinhança se torno um pouco mais complexa entre eles, uma vez que um dos roteadores se encontra ligado aos dois demais. Por tanto, um dos arquivo BGPs (no caso o que representa o roteador de São Paulo) contém mais de um "vizinho".</p>
<p>Porém uma parte adicional precisou ser desenvolvida para esse laboratório. Como havia a necessidade de atribuir IP's dinamicamente entre os links das sub-redes, precisavamos criar um DHCP Server para cada sub-rede, que seria responsável pelas requisições de IP das mesmas. Para isso foram criadas as configurações necessárias para definir o intervalo e a mascara de cada sub-rede e então inicializados todos os DHCP Servers.</p>
<p>Foi necessário adicionar um delay de 7 segundos após o start dos DHCP Servers para que as requisições dos clientes fossem atendidas corretamente.</p>
<p>O processo de modelagem da topologia pode ser visto no arquivo "lab3.py" disponível em: https://github.com/falcaopetri/redes/blob/master/projeto2/lab3/lab3.py</p>
<p>O processo de configuração dos roteadores por Zebra e BGP (um arquivo de configuração de cada um dos tipos para cada roteador, totalizando seis arquivos no caso) pode ser visto no diretório "conf" disponível em: https://github.com/falcaopetri/redes/tree/master/projeto2/lab3/conf</p>
<p>O processo de inicialização dos roteadores com as configurações especificadas pode ser visto no arquivo "util.py" disponível em: https://github.com/falcaopetri/redes/blob/master/projeto2/lab3/util.py</p>
<p>O processo de configuração e inicialização dos DHCP Servers pode ser visto no arquivo "dhcp.py" disponível em: https://github.com/falcaopetri/redes/blob/master/projeto2/lab3/dhcp.py</p>


##Dificuldades Encontradas:

<p>As dificuldades encontradas se deram básicamente de maneira incremental a cada laboratório. Sendo as principais dúvidas relacionadas a configuração do roteador por Zebra e BGP e posteriormente a configuração dos DHCP Servers.</p>
<p>As dúvidas foram sanadas por pesquisas, mas principalmente por um estudo cauteloso dos arquivos disponibilizados no laboratório em sala de aula. Apesar de no laboratório terem um propósito diferente de, no caso, simular ataques, o estudos em cima dos arquivos de configuração nos deram uma ideia clara de como os criar com os parametros que satisfizessem nossa demanda.</p>
<p>Por fim outra grande dificuldade foi quanto ao comando "pingall". Quando executado o comando não retorna as ligações de imediato, porém se "pingarmos" os links individualmente de maneira manual os links se demonstram efetivos e mais, a posterior execução do comando "pingall" retorna todos os links. Ao procurar o professor para perguntar sobre o tema, obtivemos como resposta que uma possível razão para tal é a falta de excitação necessária na rede. </p>
<p>No Lab3 não existe o mesmo problema do "pingall". Como temos os clientes fazendo DHCP Requests, acreditamos sejam escitação suficiente da rede. Sendo assim, quando executado o comando já retorna todas as ligações.</p>

##Curiosidades:

<p>Um TODO interessante seria bloquear o acesso de cada DHCP server a partir de outras sub-redeses, uma vez que, por mais que os DHCP Requests atuem somento no domínio de broadcast (que está isolado pelos routers) ainda é possível "pingar" o DHCP Server de outra sub-rede caso se conheça o IP dele.</p>
