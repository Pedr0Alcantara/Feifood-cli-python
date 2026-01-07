import os  # importa o módulo para operações com sistema de arquivos (caminhos, diretórios, etc.)
import sys  # importa o módulo para interagir com o interpretador (ex.: sys.exit)

DATA_DIR = os.path.join(os.path.dirname(__file__), "FeiArquivos")  # define a pasta de dados relativa ao arquivo atual
USERS_FILE = os.path.join(DATA_DIR, "usuarios.txt")  # caminho completo para o arquivo de usuários
MENU_FILE = os.path.join(DATA_DIR, "cardapio.txt")  # caminho completo para o arquivo do cardápio
ORDERS_FILE = os.path.join(DATA_DIR, "pedidos.txt")  # caminho completo para o arquivo de pedidos

def garantir_arquivos_de_dados():  # função que garante existência da pasta e arquivos iniciais
    os.makedirs(DATA_DIR, exist_ok=True)  # cria a pasta DATA_DIR se não existir (exist_ok evita erro se já existir)
    if not os.path.exists(USERS_FILE):  # se o arquivo de usuários não existir
        with open(USERS_FILE, "w", encoding="utf-8") as f:  # cria o arquivo de usuários (vazio)
            f.write("")  # escreve nada (cria o arquivo)
    default_menu = [  # lista padrão de itens do cardápio (tuplas nome, preço)
        ("Hamburguer", 15.00), ("Pizza", 30.00), ("Suco", 5.50), ("Batata Frita", 12.00),
        ("Refrigerante", 6.00), ("Coxinha", 7.50), ("Pastel", 8.00), ("Salada", 14.00),
        ("Hot Dog", 10.00), ("Lasanha", 28.00), ("Esfiha", 6.50), ("Kibe", 7.00),
        ("Sorvete", 9.00), ("Milkshake", 12.50), ("Torta", 11.00), ("Pão de Queijo", 5.00),
        ("Café", 4.00), ("Chá", 3.50), ("Açaí", 15.50), ("Brownie", 10.50), ("Panqueca", 16.00)
    ]
    if not os.path.exists(MENU_FILE):  # se o arquivo do cardápio não existir
        with open(MENU_FILE, "w", encoding="utf-8") as f:  # cria o arquivo do cardápio
            for name, price in default_menu:  # escreve cada item padrão no arquivo
                f.write(f"{name},{price:.2f}\n")  # formata como "Nome,Preço" com 2 casas decimais
    else:
        existing = []  # lista para armazenar nomes já existentes (em minúsculas)
        with open(MENU_FILE, "r", encoding="utf-8") as f:  # abre o cardápio existente para leitura
            for line in f:  # percorre cada linha do arquivo
                line = line.strip()  # remove espaços e quebras de linha
                if not line:  # pula linhas vazias
                    continue
                parts = line.split(",")  # separa por vírgula (espera-se "nome,preço")
                if len(parts) == 2:  # se estrutura esperada
                    existing.append(parts[0].strip().lower())  # adiciona nome em minúsculas à lista existing
        if len(existing) < 20:  # se houver menos de 20 itens, completa com os itens padrão que faltarem
            with open(MENU_FILE, "a", encoding="utf-8") as f:  # abre em modo append para adicionar novos itens
                for name, price in default_menu:  # percorre itens padrões
                    if name.lower() not in existing:  # somente adiciona se não estiver presente
                        f.write(f"{name},{price:.2f}\n")  # escreve o item que falta
    if not os.path.exists(ORDERS_FILE):  # se o arquivo de pedidos não existir
        with open(ORDERS_FILE, "w", encoding="utf-8") as f:  # cria o arquivo de pedidos (vazio)
            f.write("")  # escreve nada (cria o arquivo)

def carregar_usuarios():  # lê o arquivo de usuários e retorna uma lista de dicionários de usuários
    usuarios = []  # lista que armazenará os usuários lidos
    if not os.path.exists(USERS_FILE):  # se o arquivo não existir, retorna a lista vazia
        return usuarios
    with open(USERS_FILE, "r", encoding="utf-8") as f:  # abre o arquivo de usuários para leitura
        for line in f:  # percorre cada linha do arquivo
            line = line.strip()  # remove espaços e quebras de linha
            if not line:  # pula linhas vazias
                continue
            parts = [p.strip() for p in line.split(",")]  # divide por vírgula e remove espaços
            if len(parts) == 3:  # formato esperado: username, email, password
                username, email, password = parts  # desempacota as três partes
            elif len(parts) == 2:  # caso antigo ou sem e-mail: username, password
                username, password = parts  # desempacota as duas partes
                email = None  # atribui None para email ausente
            else:
                continue  # linha com formato inválido é ignorada
            usuarios.append({
                "usuario": username,  # nome do usuário conforme no arquivo
                "usuario_key": username.lower().strip(),  # chave de busca (lower + strip)
                "email": email,  # email (ou None)
                "email_key": (email.lower().strip() if email else None),  # chave de email ou None
                "senha": password,  # senha em texto (atenção à segurança: não é ideal armazenar em texto)
            })
    return usuarios  # retorna a lista de usuários

def encontrar_usuario_por_nome(users: list, username: str):  # busca usuários pela chave de nome
    key = username.lower().strip()  # normaliza termo de busca
    return [u for u in users if u.get("usuario_key") == key]  # retorna lista de usuários que batem exatamente

def encontrar_usuario_por_email(users: list, email: str):  # busca usuários pela chave de email
    ekey = email.lower().strip()  # normaliza email
    return [u for u in users if u.get("email_key") == ekey]  # retorna lista de usuários que batem exatamente

def salvar_usuario(username: str, password: str, email: str) -> bool:  # adiciona um usuário novo ao arquivo
    with open(USERS_FILE, "a", encoding="utf-8") as f:  # abre o arquivo em modo append
        f.write(f"{username},{email},{password}\n")  # escreve uma linha com username,email,senha
    return True  # retorna True indicando sucesso (sempre retorna True no estado atual)

def autenticar(username: str, email: str, password: str) -> bool:  # tenta autenticar combinando 3 campos
    users = carregar_usuarios()  # carrega usuários do arquivo
    ukey = username.lower().strip()  # normaliza username para comparação
    ekey = email.lower().strip()  # normaliza email para comparação
    for u in users:  # percorre todos os usuários carregados
        if u.get("usuario_key") == ukey and u.get("email_key") == ekey and u.get("senha") == password:
            return True  # retorna True se username, email e senha baterem
    return False  # retorna False se não encontrou correspondência

def carregar_cardapio():  # carrega o cardápio do arquivo e o retorna como dicionário
    menu = {}  # dicionário resultado: chave = nome.lower(), valor = {"name": nome, "price": preço}
    if not os.path.exists(MENU_FILE):  # se arquivo não existir, retorna dicionário vazio
        return menu
    with open(MENU_FILE, "r", encoding="utf-8") as f:  # abre o arquivo do cardápio
        for line in f:  # percorre cada linha
            line = line.strip()  # remove espaços/breaks
            if not line:  # pula linhas vazias
                continue
            parts = line.split(",")  # separa por vírgula -> [nome, preço]
            if len(parts) != 2:  # se o formato não for o esperado, pula a linha
                continue
            name, price_str = parts[0].strip(), parts[1].strip()  # extrai nome e preço como string
            try:
                price = float(price_str)  # tenta converter preço para float
            except ValueError:
                continue  # pula se preço inválido
            menu[name.lower()] = {"name": name, "price": price}  # armazena no dicionário com chave em minúsculas
    return menu  # retorna o dicionário do cardápio

def buscar_alimento(menu: dict, term: str):  # busca itens no cardápio que contenham o termo (case-insensitive)
    term = term.lower().strip()  # normaliza termo de busca
    results = []  # lista de resultados
    for key, item in menu.items():  # percorre itens do menu (key é nome em minúsculas)
        if term in key:  # se o termo aparece na chave (nome)
            results.append(item)  # adiciona o item aos resultados
    def chave_nome(item):  # função auxiliar para ordenar por nome do item
        return item["name"]
    return sorted(results, key=chave_nome)  # retorna resultados ordenados alfabeticamente pelo nome

def carregar_pedidos():  # carrega pedidos do arquivo e retorna lista de dicionários
    orders = []  # lista que conterá pedidos
    if not os.path.exists(ORDERS_FILE):  # se arquivo de pedidos não existir, retorna lista vazia
        return orders
    with open(ORDERS_FILE, "r", encoding="utf-8") as f:  # abre arquivo de pedidos para leitura
        for line in f:  # percorre cada linha do arquivo
            line = line.strip()  # remove espaços e quebras de linha
            if not line:  # pula linhas vazias
                continue
            parts = line.split("|")  # separa campos por pipe: id|user|items|total|rating|paid
            if len(parts) not in (5, 6):  # aceita 5 ou 6 partes (compatibilidade)
                continue
            oid_str, username, items_str, total_str, rating_str = parts[:5]  # desempacota as primeiras 5 partes
            paid_str = parts[5] if len(parts) == 6 else "0"  # se houver 6ª parte, é o paid; caso contrário assume "0"
            try:
                oid = int(oid_str)  # converte id para int
                total = float(total_str)  # converte total para float
                rating = float(rating_str) if rating_str.strip() != "" else None  # rating pode ser vazio => None
                paid = True if paid_str.strip() == "1" else False  # paid é "1" => True, caso contrário False
            except ValueError:
                continue  # pula linhas com valores mal formatados
            items = {}  # dicionário para armazenar itens do pedido
            items_str = items_str.strip()  # strip nos itens
            if items_str:  # se houver itens
                for pair in items_str.split(","):  # cada par tem formato "Nome:quantidade"
                    if not pair:
                        continue
                    if ":" not in pair:  # ignora pares sem separador ":"
                        continue
                    name, qty_str = pair.split(":", 1)  # split apenas no primeiro ":" (nome pode conter :)
                    try:
                        qty = int(qty_str)  # converte quantidade para int
                    except ValueError:
                        continue  # pula se quantidade inválida
                    items[name] = qty  # armazena no dicionário items
            orders.append({  # adiciona o pedido convertido para a lista orders
                "id": oid,
                "user": username,
                "items": items,
                "total": total,
                "rating": rating,
                "paid": paid,
            })
    return orders  # retorna a lista de pedidos

def salvar_pedidos(orders):  # salva a lista de pedidos no arquivo (sobrescreve todo arquivo)
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:  # abre arquivo em modo escrita (sobrescreve)
        for o in orders:  # percorre cada pedido
            items_str = ",".join([f"{name}:{qty}" for name, qty in o["items"].items()])  # converte items para string "Nome:qty,..."
            rating_str = str(o["rating"]) if o["rating"] is not None else ""  # prepara rating (string ou vazio)
            paid_str = "1" if o.get("paid") else "0"  # converte boolean paid para "1" ou "0"
            f.write(f"{o['id']}|{o['user']}|{items_str}|{o['total']}|{rating_str}|{paid_str}\n")  # escreve linha formatada

def proximo_id_pedido(orders):  # calcula o próximo id de pedido disponível
    if not orders:  # se não houver pedidos, começa em 1
        return 1
    return max(o["id"] for o in orders) + 1  # retorna max id existente + 1

def calcular_total(items: dict, menu: dict) -> float:  # calcula o total do pedido baseado nas quantidades e preços do menu
    total = 0.0  # soma inicial
    for name, qty in items.items():  # percorre itens (nome e quantidade)
        entry = menu.get(name.lower())  # busca entrada no menu por chave minúscula
        if entry:  # se item existe no menu
            total += entry["price"] * qty  # acumula preço * quantidade
    return round(total, 2)  # retorna total arredondado para 2 casas decimais

def imprimir_lista_alimentos(items):  # imprime lista de alimentos (resultado de busca)
    if not items:  # se lista vazia, informa que nada foi encontrado
        print("Nenhum alimento encontrado.")
        return
    print("Alimentos encontrados:")  # cabeçalho
    for idx, it in enumerate(items, start=1):  # imprime cada item com índice e preço
        print(f"{idx}) {it['name']} (R$ {it['price']:.2f})")

def pedir_inteiro(msg, allow_empty=False):  # solicita ao usuário um inteiro via input, com repetição até valido
    while True:
        val = input(msg).strip()  # lê e faz strip
        if allow_empty and val == "":  # se vazio permitido e usuário deixou em branco, retorna None
            return None
        try:
            return int(val)  # tenta converter para inteiro e retorna
        except ValueError:
            print("Digite um número inteiro válido.")  # mensagem de erro e repete loop

def pedir_float(msg, allow_empty=False):  # solicita um número decimal (float) com tratamento de vírgula
    while True:
        val = input(msg).strip()  # lê input e strip
        if allow_empty and val == "":  # aceita vazio se allow_empty True
            return None
        try:
            val = val.replace(",", ".")  # permite que usuário use vírgula como separador decimal
            return float(val)  # converte e retorna float
        except ValueError:
            print("Digite um número válido (pode ser decimal).")  # mensagem de erro

def pedir_nao_vazio(msg, allow_empty=False):  # solicita uma string não vazia
    while True:
        val = input(msg).strip()  # lê input e strip
        if allow_empty and val == "":  # retorna None se vazio permitido
            return None
        if val:  # se string não vazia, retorna
            return val
        print("O valor não pode ser vazio.")  # caso contrário avisa e repete

def pedir_apenas_letras(msg, allow_empty=False):  # solicita string contendo somente letras e espaços
    while True:
        val = input(msg).strip()  # lê input
        if allow_empty and val == "":  # aceita vazio se permitido
            return None
        if val and all(ch.isalpha() or ch.isspace() for ch in val):  # verifica se todos os caracteres são letras ou espaço
            return val  # retorna se válido
        print("Digite apenas letras (sem números ou caracteres especiais).")  # erro se inválido

def pedir_opcao_menu(valid_options, allow_empty=False):  # lê opção de menu (apenas números permitidos)
    valid_set = {str(v) for v in valid_options}  # cria conjunto de opções válidas como strings
    while True:
        val = input("Opção: ").strip()  # lê input
        if allow_empty and val == "":  # aceita vazio se permitido
            return None
        if val.isdigit() and val in valid_set:  # verifica se é dígito e está no conjunto válido
            return val  # retorna a opção (string)
        print("Opção inválida. Digite apenas números das opções.")  # mensagem de erro

def imprimir_cardapio_numerado(menu: dict):  # imprime o cardápio numerado e retorna a lista de itens (valores)
    items = [v for v in menu.values()]  # lista dos valores do dicionário menu (cada um tem 'name' e 'price')
    print("\n=== Cardápio ===")  # cabeçalho
    for idx, it in enumerate(items, start=1):  # imprime cada item com índice e preço formatado
        print(f"{idx}) {it['name']} - R$ {it['price']:.2f}")
    return items  # retorna a lista ordenada conforme foi percorrida

def ler_lista_numeros(msg, max_index, allow_empty=False):  # lê uma lista de números separados por vírgula e valida índices
    while True:
        raw = input(msg).strip()  # lê input
        if allow_empty and raw == "":  # se vazio permitido, retorna None
            return None
        if not raw:
            print("Entrada vazia. Digite números separados por vírgula ou pressione Enter para voltar.")  # pede nova tentativa
            continue
        parts = [p.strip() for p in raw.split(",") if p.strip()]  # separa por vírgula e remove vazios
        if not parts:
            print("Entrada inválida. Tente novamente.")  # se sem partes válidas, repete
            continue
        if all(p.isdigit() for p in parts):  # verifica se todas as partes são números
            nums = [int(p) for p in parts]  # converte para inteiros
            if all(1 <= n <= max_index for n in nums):  # valida intervalo dos índices
                return nums  # retorna lista de inteiros válida
        print("Use apenas números válidos, separados por vírgula, conforme o cardápio.")  # mensagem de erro

def ler_itens_com_quantidade(msg, max_index, allow_empty=False):  # lê itens possivelmente com quantidade (ex: 2x3, 4)
    while True:
        raw = input(msg).strip()  # lê input
        if allow_empty and raw == "":  # aceita vazio se permitido
            return None
        if not raw:
            print("Entrada vazia. Digite números separados por vírgula (ex: 2,1,4) ou com quantidade (ex: 2x5,4x1).")
            continue
        parts = [p.strip() for p in raw.split(",") if p.strip()]  # separa por vírgula
        if not parts:
            print("Entrada inválida. Tente novamente.")
            continue
        result = []  # lista de tuplas (idx, qty)
        ok = True  # flag para controlar validade
        for p in parts:  # processa cada parte
            if any(sep in p for sep in ("x", "*", ":")):  # detecta formatos com separador de quantidade
                for sep in ("x", "*", ":"):  # tenta cada separador possível
                    if sep in p:
                        left, right = p.split(sep, 1)  # divide na primeira ocorrência do separador
                        break
                if not left.isdigit() or not right.isdigit():  # valida que ambos são dígitos
                    ok = False
                    break
                idx = int(left)  # índice do item
                qty = int(right)  # quantidade
            else:
                if not p.isdigit():  # caso sem separador, deve ser número simples
                    ok = False
                    break
                idx = int(p)  # índice
                qty = 1  # quantidade padrão 1
            if not (1 <= idx <= max_index) or qty <= 0:  # valida intervalo do índice e quantidade positiva
                ok = False
                break
            result.append((idx, qty))  # adiciona tupla (índice, quantidade)
        if ok:
            return result  # retorna lista válida
        print("Use índices válidos (conforme cardápio) e quantidades >= 1. Ex: 2,1,4 ou 2x5,4x1.")  # erro e repete

def pedir_email_valido(msg, allow_empty=False):  # lê e valida um e-mail simples (verificação básica)
    while True:
        val = input(msg).strip()  # lê input
        if allow_empty and val == "":  # aceita vazio se permitido
            return None
        if val == "":  # se vazio e não permitido, avisa
            print("E-mail não pode ser vazio.")
            continue
        if "@" in val and "." in val and " " not in val:  # checagem simples: contém @ e . e sem espaços
            return val  # retorna email válido
        print("E-mail inválido. Ex: nome@dominio.com")  # mensagem de erro

def fluxo_cadastrar_usuario():  # fluxo interativo para cadastrar novo usuário
    print("\n=== Cadastrar novo usuário ===")  # cabeçalho
    username = pedir_apenas_letras("Usuário (apenas letras, Enter para voltar): ", allow_empty=True)  # solicita username
    if username is None:  # se usuário pressionou Enter para voltar
        return
    email = pedir_email_valido("E-mail (Enter para voltar): ", allow_empty=True)  # solicita email
    if email is None:
        return
    password = pedir_nao_vazio("Senha (qualquer caractere, Enter para voltar): ", allow_empty=True)  # solicita senha
    if password is None:
        return
    salvar_usuario(username, password, email)  # salva usuário no arquivo
    print("Usuário cadastrado com sucesso!")  # confirma cadastro

def fluxo_login_usuario():  # fluxo interativo de login que exige nome + e-mail + senha
    print("\n=== Login (nome + e-mail + senha) ===")  # cabeçalho
    username = pedir_apenas_letras("Usuário (apenas letras, Enter para voltar): ", allow_empty=True)  # solicita username
    if username is None:
        return None
    email = pedir_email_valido("E-mail (Enter para voltar): ", allow_empty=True)  # solicita email
    if email is None:
        return None
    password = pedir_nao_vazio("Senha (qualquer caractere, Enter para voltar): ", allow_empty=True)  # solicita senha
    if password is None:
        return None
    if autenticar(username, email, password):  # tenta autenticar com os três campos
        print("Login realizado!")
        return username.lower().strip()  # retorna username normalizado em lowercase
    print("Usuário/e-mail/senha inválidos ou usuário sem e-mail cadastrado.")  # mensagem em caso de falha
    return None  # retorna None se falhou

def fluxo_busca(menu):  # fluxo interativo para buscar alimento no cardápio
    term = pedir_nao_vazio("Buscar por alimento (termo): ")  # solicita termo de busca
    results = buscar_alimento(menu, term)  # busca no dicionário do menu
    imprimir_lista_alimentos(results)  # imprime os resultados

def listar_meus_pedidos(username, orders):  # lista os pedidos pertencentes ao usuário fornecido
    mine = [o for o in orders if o["user"] == username]  # filtra pedidos do usuário
    if not mine:
        print("Você não possui pedidos.")  # avisa se nenhum pedido encontrado
        return []
    print("\n=== Meus pedidos ===")  # cabeçalho
    for i, o in enumerate(mine, start=1):  # para cada pedido do usuário, imprime detalhes
        items_desc = ", ".join([f"{name} x{qty}" for name, qty in o["items"].items()]) or "(vazio)"  # descrição itens
        rating_desc = o["rating"] if o["rating"] is not None else "(sem avaliação)"  # descrição de avaliação
        paid_desc = "(pago)" if o.get("paid") else "(não pago)"  # descrição de pagamento
        print(f"Pedido {i} | ID {o['id']} | Itens: {items_desc} | Total: R$ {o['total']:.2f} | Avaliação: {rating_desc} {paid_desc}")
    return mine  # retorna lista com os pedidos do usuário

def criar_pedido(username, orders, menu):  # cria um novo pedido para o usuário
    oid = proximo_id_pedido(orders)  # pega próximo id livre
    temp_order = {"id": oid, "user": username, "items": {}, "total": 0.0, "rating": None, "paid": False}  # estrutura temporária do pedido
    print(f"Pedido criado com ID {oid}.")  # informa id criado
    items_list = imprimir_cardapio_numerado(menu)  # imprime cardápio e recebe lista ordenada de itens
    max_index = len(items_list)  # quantidade de itens no cardápio
    added_any = False  # flag para verificar se adicionou ao menos um item
    while True:  # loop para adicionar itens até o usuário sair
        entries = ler_itens_com_quantidade(
            "Digite os itens por número (ex: 2,1,4) ou com quantidade (ex: 2x20,4x3). Enter para voltar: ",
            max_index,
            allow_empty=True,
        )  # lê entradas do usuário
        if entries is None:  # se usuário optou por voltar (Enter), sai do loop
            break
        for idx, qty in entries:  # para cada entrada (índice, quantidade)
            item_name = items_list[idx - 1]["name"]  # pega nome do item pelo índice (ajusta -1)
            temp_order["items"][item_name] = temp_order["items"].get(item_name, 0) + qty  # acumula quantidade no pedido
            added_any = True  # marca que adicionou algo
        temp_order["total"] = calcular_total(temp_order["items"], menu)  # recalcula total do pedido
        print(f"Itens atuais: {', '.join([f'{n} x{q}' for n, q in temp_order['items'].items()])} | Total: R$ {temp_order['total']:.2f}")
        cont = input("Deseja continuar adicionando itens? (s/n, Enter para sair): ").strip().lower()  # pergunta se continua
        if cont == "" or cont == "n":  # se vazio ou 'n', sai
            break
        elif cont != "s":  # se resposta inválida, informa e repete
            print("Resposta inválida. Use 's', 'n' ou Enter.")
    if not added_any:  # se não adicionou nenhum item, cancela pedido
        print("Pedido cancelado. Voltando.")
        return
    orders.append(temp_order)  # adiciona pedido à lista de pedidos
    salvar_pedidos(orders)  # salva pedidos atualizados no arquivo
    print("Pedido finalizado (você pode editar depois).")  # confirma finalização

def editar_itens_pedido(username, orders, menu):  # permite editar itens de um pedido do usuário
    mine = listar_meus_pedidos(username, orders)  # lista pedidos do usuário
    if not mine:
        return
    idx = pedir_inteiro("Editar qual pedido (número da lista, Enter para voltar): ", allow_empty=True)  # pergunta qual pedido editar
    if idx is None:
        return
    if idx < 1 or idx > len(mine):  # valida índice escolhido
        print("Pedido inválido.")
        return
    order = mine[idx - 1]  # seleciona pedido a editar
    while True:  # loop de edição (adicionar/remover/voltar)
        print("\n1) Adicionar itens (lista, ex: 2,1,4 ou 2x5,4x1)\n2) Remover quantidades de itens (lista, ex: 2,1,4 ou 2x3)\n3) Voltar")
        opt = pedir_opcao_menu([1, 2, 3], allow_empty=True)  # lê opção do menu interno
        if opt is None:
            break
        items_list = imprimir_cardapio_numerado(menu)  # reimprime cardápio para referência
        max_index = len(items_list)
        if opt == "1":  # adicionar itens
            entries = ler_itens_com_quantidade(
                "Itens para adicionar (ex: 2,1,4 ou 2x5,4x1). Enter para voltar: ",
                max_index,
                allow_empty=True,
            )
            if entries is None:
                pass
            else:
                for idx, qty in entries:  # adiciona as quantidades ao pedido
                    item_name = items_list[idx - 1]["name"]
                    order["items"][item_name] = order["items"].get(item_name, 0) + qty
        elif opt == "2":  # remover quantidades
            entries = ler_itens_com_quantidade(
                "Itens para remover (ex: 2,1,4 ou 2x3). Enter para voltar: ",
                max_index,
                allow_empty=True,
            )
            if entries is None:
                pass
            else:
                for idx, qty in entries:
                    item_name = items_list[idx - 1]["name"]
                    if item_name in order["items"]:  # se item está no pedido
                        current = order["items"].get(item_name, 0)  # quantidade atual
                        new_qty = current - qty  # nova quantidade após remoção
                        if new_qty <= 0:  # se zerou ou ficou negativo, remove o item
                            del order["items"][item_name]
                        else:
                            order["items"][item_name] = new_qty  # atualiza quantidade
                    else:
                        print(f"Item '{item_name}' não está no pedido.")  # aviso se item não estava no pedido
        elif opt == "3":  # voltar
            break
        order["total"] = calcular_total(order["items"], menu)  # recalcula total após alterações
        itens_str = ", ".join([f"{n} x{q}" for n, q in order["items"].items()]) or "(vazio)"  # monta string de itens
        print(f"Itens atuais: {itens_str} | Total: R$ {order['total']:.2f}")  # mostra estado atual do pedido
    salvar_pedidos(orders)  # salva pedidos atualizados no arquivo
    print("Pedido atualizado.")  # confirma atualização

def excluir_pedido(username, orders):  # exclui um pedido do usuário
    mine = listar_meus_pedidos(username, orders)  # lista pedidos do usuário
    if not mine:
        return
    idx = pedir_inteiro("Excluir qual pedido (número da lista, Enter para voltar): ", allow_empty=True)  # pergunta qual excluir
    if idx is None:
        return
    if idx < 1 or idx > len(mine):  # valida índice
        print("Pedido inválido.")
        return
    order = mine[idx - 1]  # seleciona pedido a excluir
    confirm = input("Continuar? (s/n): ").strip().lower()  # confirma exclusão
    if confirm == "s":  # se confirmado
        orders.remove(order)  # remove da lista
        salvar_pedidos(orders)  # salva alterações
        print("Pedido excluído.")  # informa exclusão
    else:
        print("Exclusão cancelada.")  # cancela se não confirmado

def avaliar_pedido(username, orders):  # permite avaliar um pedido (nota 0 a 5)
    mine = listar_meus_pedidos(username, orders)  # lista pedidos do usuário
    if not mine:
        return
    idx = pedir_inteiro("Avaliar qual pedido (número da lista, Enter para voltar): ", allow_empty=True)  # pergunta qual avaliar
    if idx is None:
        return
    if idx < 1 or idx > len(mine):  # valida índice
        print("Pedido inválido.")
        return
    order = mine[idx - 1]  # seleciona pedido
    rating = pedir_float("Nota (0 a 5, pode ser decimal; vazio para remover): ", allow_empty=True)  # pede nota
    if rating is None:
        order["rating"] = None  # remove avaliação se vazio
    elif 0 <= rating <= 5:  # valida intervalo 0-5
        order["rating"] = rating  # atribui avaliação
    else:
        print("Nota inválida.")  # mensagem de erro
        return
    salvar_pedidos(orders)  # salva alterações
    print("Avaliação registrada.")  # confirma

def pagar_pedido(username, orders):  # fluxo de pagamento de pedido
    mine = listar_meus_pedidos(username, orders)  # lista pedidos do usuário
    if not mine:
        return
    idx = pedir_inteiro("Pagar qual pedido (número da lista, Enter para voltar): ", allow_empty=True)  # pergunta qual pagar
    if idx is None:
        return
    if idx < 1 or idx > len(mine):  # valida índice
        print("Pedido inválido.")
        return
    order = mine[idx - 1]  # seleciona pedido
    if not order["items"]:  # se pedido vazio, informa que precisa adicionar itens
        print("Pedido vazio, adicione itens antes de pagar.")
        return
    if order.get("paid"):  # se já pago, informa
        print("Este pedido já está pago.")
        return
    print(f"Total a pagar: R$ {order['total']:.2f}")  # mostra total a pagar
    print("1) PIX\n2) Cartão\n3) Dinheiro\n(Enter para voltar)")  # opções de pagamento
    opt = pedir_opcao_menu([1, 2, 3], allow_empty=True)  # lê opção
    if opt is None:
        print("Pagamento cancelado.")  # cancela se Enter
        return
    elif opt == "1":
        print("Chave PIX: feifood@exemplo.com")  # mensagem para PIX (simulada)
    elif opt == "2":
        print("Pagamento no cartão processado")  # mensagem simulada de cartão
    elif opt == "3":
        print("Pagamento em dinheiro registrado")  # mensagem simulada de dinheiro
    confirmar = input("Confirmar pagamento? (s/n, Enter para voltar): ").strip().lower()  # confirmação final
    if confirmar == "":
        print("Pagamento cancelado.")  # cancela se Enter
        return
    if confirmar != "s":
        print("Pagamento não confirmado.")  # se não 's', cancela
        return
    order["paid"] = True  # marca pedido como pago
    salvar_pedidos(orders)  # salva alterações
    print("Pagamento concluído.")  # confirma

def menu_pedidos(username, menu):  # menu interativo para gerenciar pedidos do usuário logado
    while True:
        orders = carregar_pedidos()  # carrega pedidos atualizados do arquivo a cada iteração
        print("\n=== Pedidos ===")  # cabeçalho
        print("1) Criar pedido")
        print("2) Editar itens do pedido")
        print("3) Excluir pedido")
        print("4) Listar meus pedidos")
        print("5) Avaliar pedido")
        print("6) Pagar pedido")
        print("7) Voltar (Enter também volta)")
        opt = pedir_opcao_menu([1, 2, 3, 4, 5, 6, 7], allow_empty=True)  # lê opção do menu de pedidos
        if opt is None:
            return  # volta para menu anterior se Enter
        if opt == "1":
            criar_pedido(username, orders, menu)  # chama criar pedido
        elif opt == "2":
            editar_itens_pedido(username, orders, menu)  # chama editar itens
        elif opt == "3":
            excluir_pedido(username, orders)  # chama excluir pedido
        elif opt == "4":
            listar_meus_pedidos(username, orders)  # lista pedidos do usuário
        elif opt == "5":
            avaliar_pedido(username, orders)  # chama avaliar
        elif opt == "6":
            pagar_pedido(username, orders)  # chama pagar
        elif opt == "7":
            return  # volta ao menu anterior

def menu_principal():  # função principal que exibe o menu principal do sistema
    garantir_arquivos_de_dados()  # garante que pasta e arquivos existem antes de iniciar
    menu = carregar_cardapio()  # carrega cardápio inicial
    logged_user = None  # variável que guarda usuário logado (None se ninguém logado)
    while True:  # loop principal do menu
        print("\n=== FEIFood ===")  # título
        if not logged_user:  # se ninguém logado, mostra opções públicas
            print("1) Cadastrar novo usuário")
            print("2) Login")
            print("3) Sair")
            opt = pedir_opcao_menu([1, 2, 3])  # lê opção principal
            if opt == "1":
                fluxo_cadastrar_usuario()  # fluxo de cadastro
            elif opt == "2":
                logged_user = fluxo_login_usuario()  # fluxo de login, atribui usuário logado (ou None)
            elif opt == "3":
                print("Encerrando...")  # mensagem de saída
                break  # encerra loop principal
        else:  # se já existe usuário logado, mostra menu privado
            print(f"Usuário logado: {logged_user}")  # mostra nome do usuário logado
            print("1) Listar cardápio completo")
            print("2) Buscar por alimento")
            print("3) Gerenciar pedidos")
            print("4) Logout")
            print("0) Sair")
            opt = pedir_opcao_menu([0, 1, 2, 3, 4])  # lê opção para usuários logados
            if opt == "1":
                menu = carregar_cardapio()  # recarrega cardápio (pode ter sido atualizado externamente)
                imprimir_cardapio_numerado(menu)  # imprime cardápio numerado
            elif opt == "2":
                menu = carregar_cardapio()  # recarrega cardápio
                fluxo_busca(menu)  # chama fluxo de busca
            elif opt == "3":
                menu = carregar_cardapio()  # recarrega cardápio
                menu_pedidos(logged_user, menu)  # entra no menu de pedidos do usuário
            elif opt == "4":
                logged_user = None  # faz logout (zera variável)
                print("Logout realizado.")  # confirma logout
            elif opt == "0":
                print("Encerrando...")  # mensagem de saída
                break  # encerra loop principal

if __name__ == "__main__":  # ponto de entrada quando o script é executado diretamente
    try:
        menu_principal()  # executa função principal do programa
    except KeyboardInterrupt:  # captura interrupção por Ctrl+C
        print("\nEncerrado.")  # imprime mensagem de encerramento amigável
        sys.exit(0)  # sai do programa com código 0 (sem erro)
