class robot:
    def __init__(self):
        #inicializacao dos sensores, motores e objetos
        self.motorDireita = LargeMotor(OUTPUT_A)
        self.motorEsquerda = LargeMotor(OUTPUT_C)
        """
        self.sensor1 = #cor, apontado p/chao(ajuste)
        self.sensor2 = #cor, apontado p/chao(ajuste)
        """

    def andar(self, velocidade = VELOCIDADE):
      self.motorDireita.run_forever(speed_sp = velocidade)
      self.motorEsquerda.run_forever(speed_sp = velocidade)

    def parar(self, action):
      self.motorDireita.stop(stop_action = action)
      self.motorEsquerda.stop(stop_action = action)
    
    def alinhar(self, cor = NoColor, direcao = 1):
      while True:
            if self.cor(self.sensor1.raw) != cor:
                self.motorEsquerda.run_forever(speed_sp=200 * direcao)
            else:
                self.motorEsquerda.stop(stop_action='hold')
            if self.cor(self.sensor2.raw) != cor:
                self.motorDireita.run_forever(speed_sp=200 * direcao)
            else:
                self.motorDireita.stop(stop_action='hold')
            if self.cor(self.sensor1.raw) == cor and self.cor(
                    self.sensor2.raw) == cor:
                self.parar('hold')
                break

    def curva_esquerda(self, rotacoes, velocidade):
        #90* p/ esquerda com 1 motor; velocidade de 0 a 100, representando a porcentagem da forca do motor
        self.motorDireita.stop()
        self.motorEsquerda.on_for_rotations(SpeedPercent(velocidade), rotacoes)
        self.motorEsquerda.stop()

    def curva_direita(self, rotacoes, velocidade):
        #90* p/ direita com 1 motor; velocidade de 0 a 100, representando a porcentagem da forca do motor
        self.motorEsquerda.stop()
        self.motorDireita.on_for_rotations(SpeedPercent(velocidade), rotacoes)
        self.motorDireita.stop()

    def anda_enquanto_cor(self, cor, velocidade):
        #Anda a uma dada velocidade enquanto ve uma dada cor >>> os parametros sao a cor e a velocidade dos motores
        while cor == self.cor(self.sensor1.raw) and cor == self.cor(
                self.sensor2.raw):
            self.motorEsquerda.run_forever(speed_sp=velocidade)
            self.motorDireita.run_forever(speed_sp=velocidade)
        self.motorEsquerda.stop(stop_action='hold')
        self.motorEsquerda.reset()
        self.motorDireita.stop(stop_action='hold')
        self.motorDireita.reset()

    def frente_por_rotacoes(self, posicao, velocidade):
        #Vai pra frente ate uma determinada posicao do motor A >>> os parametros sao a posicao final desejada e a velocidade dos motores
        self.motorEsquerda.reset()
        self.motorDireita.reset()
        while self.motorEsquerda.position < posicao:
            self.motorEsquerda.run_forever(speed_sp=velocidade)
            self.motorDireita.run_forever(speed_sp=velocidade)
        self.motorEsquerda.stop(stop_action='hold')
        self.motorDireita.stop(stop_action='hold')

    def re_por_rotacoes(self, posicao, velocidade):
        #Vai pra tras ate uma determinada posicao do motor A >>> os parametros sao a posicao final desejada(negativa) e a velocidade dos motores(positiva)
        self.motorEsquerda.reset()
        self.motorDireita.reset()
        while self.motorEsquerda.position > posicao:
            self.motorEsquerda.run_forever(speed_sp=-velocidade)
            self.motorDireita.run_forever(speed_sp=-velocidade)
        self.motorEsquerda.stop(stop_action='hold')
        self.motorDireita.stop(stop_action='hold')

    def ajuste_direto(self, direcao):
        #Ajuste utilizando os dois motores ao mesmo tempo
        x = self.cor(self.sensor1.raw)
        while True:
            if self.cor(self.sensor1.raw) == x:
                self.motorEsquerda.run_forever(speed_sp=200 * direcao)
            else:
                self.motorEsquerda.stop(stop_action='hold')
            if self.cor(self.sensor2.raw) == x:
                self.motorDireita.run_forever(speed_sp=200 * direcao)
            else:
                self.motorDireita.stop(stop_action='hold')
            if self.cor(self.sensor1.raw) != x and self.cor(
                    self.sensor2.raw) != x:
                self.motorEsquerda.stop(stop_action='hold')
                self.motorDireita.stop(stop_action='hold')
                break

    def curva_direcao(self, x, tamanho_curva, velocidade):
        #Funcao que recebe 0 ou 1 e realiza a curva com dois motores p/ aquela direcao, sendo 0 -> direita; 1 -> esquerda
        if x == 0:
            #90* p/ direita com 2 motores
            self.motorEsquerda.reset()
            self.motorDireita.reset()
            while self.motorDireita.position < tamanho_curva:
                self.motorEsquerda.run_forever(speed_sp=-velocidade)
                self.motorDireita.run_forever(speed_sp=velocidade)
            self.motorEsquerda.stop(stop_action='hold')
            self.motorDireita.stop(stop_action='hold')
        elif x == 1:
            #90* p/ esquerda com 2 motores
            self.motorDireita.reset()
            self.motorEsquerda.reset()
            while self.motorEsquerda.position < tamanho_curva:
                self.motorEsquerda.run_forever(speed_sp=velocidade)
                self.motorDireita.run_forever(speed_sp=-velocidade)
            self.motorEsquerda.stop(stop_action='hold')
            self.motorDireita.stop(stop_action='hold')

    def cor_intervalo(self):
        #funcao que gera os intervalos de cor lidas em rgb, continuar para maior precisao na leitura de cores
        cores_lista0 = []
        cores_lista1 = []
        cores_lista2 = []
        for i in range(5):
            time.sleep(1)
            cor = list(self.sensor1.rgb)
            cores_lista0.append(cor[0])
            cores_lista1.append(cor[1])
            cores_lista2.append(cor[2])
        intervalomaior = (
            max(cores_lista0) + (max(cores_lista0) - min(cores_lista0)),
            max(cores_lista1) + (max(cores_lista1) - min(cores_lista1)),
            max(cores_lista2) + (max(cores_lista2) - min(cores_lista2)))
        intervalomenor = (
            min(cores_lista0) + (max(cores_lista0) - min(cores_lista0)),
            min(cores_lista1) + (max(cores_lista1) - min(cores_lista1)),
            min(cores_lista2) + (max(cores_lista2) - min(cores_lista2)))
        intervaloamplitude = (max(cores_lista0) - min(cores_lista0),
                              max(cores_lista1) - min(cores_lista1),
                              max(cores_lista2) - min(cores_lista2))
        print(intervalomaior)
        print(intervalomenor)
        print(intervaloamplitude)
        #criar modulo de comparacao entre intervalos obtidos e cores

    def teste_garra(self, forca, rotacoes):
        #Teste da garra: move a garra em um sentido, com uma dada forca, espera cinco segundos, e move a garra no sentido contratio, com a mesma forca
        self.motorGarra.on_for_rotations(SpeedPercent(forca), rotacoes)
        self.motorGarra.stop(stop_action='hold')
        time.sleep(5)
        self.motorGarra.on_for_rotations(SpeedPercent(forca), -rotacoes)
