import os
import sys
DATA_DIR = os.path.join(os.path.dirname(__file__), "FeiArquivos")
USERS_FILE = os.path.join(DATA_DIR, "usuarios.txt")
MENU_FILE = os.path.join(DATA_DIR, "cardapio.txt")
ORDERS_FILE = os.path.join(DATA_DIR, "pedidos.txt")

def garantir_arquivos_de_dados():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            f.write("")
    default_menu = [
        ("Hamburguer", 15.00), ("Pizza", 30.00), ("Suco", 5.50), ("Batata Frita", 12.00),
        ("Refrigerante", 6.00), ("Coxinha", 7.50), ("Pastel", 8.00), ("Salada", 14.00),
        ("Hot Dog", 10.00), ("Lasanha", 28.00), ("Esfiha", 6.50), ("Kibe", 7.00),
        ("Sorvete", 9.00), ("Milkshake", 12.50), ("Torta", 11.00), ("Pão de Queijo", 5.00),
        ("Café", 4.00), ("Chá", 3.50), ("Açaí", 15.50), ("Brownie", 10.50), ("Panqueca", 16.00)
    ]
    if not os.path.exists(MENU_FILE):
        with open(MENU_FILE, "w", encoding="utf-8") as f:
            for name, price in default_menu:
                f.write(f"{name},{price:.2f}\n")
    else:
        existing = []
        with open(MENU_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) == 2:
                    existing.append(parts[0].strip().lower())
        if len(existing) < 20:
            with open(MENU_FILE, "a", encoding="utf-8") as f:
                for name, price in default_menu:
                    if name.lower() not in existing:
                        f.write(f"{name},{price:.2f}\n")
    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "w", encoding="utf-8") as f:
            f.write("")

def carregar_usuarios():
    usuarios = []
    if not os.path.exists(USERS_FILE):
        return usuarios
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) == 3:
                username, email, password = parts
            elif len(parts) == 2:
                username, password = parts
                email = None
            else:
                continue
            usuarios.append({
                "usuario": username,
                "usuario_key": username.lower().strip(),
                "email": email,
                "email_key": (email.lower().strip() if email else None),
                "senha": password,
            })
    return usuarios

def encontrar_usuario_por_nome(users: list, username: str):
    key = username.lower().strip()
    return [u for u in users if u.get("usuario_key") == key]

def encontrar_usuario_por_email(users: list, email: str):
    ekey = email.lower().strip()
    return [u for u in users if u.get("email_key") == ekey]

def salvar_usuario(username: str, password: str, email: str) -> bool:
    with open(USERS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{username},{email},{password}\n")
    return True

def autenticar(username: str, email: str, password: str) -> bool:
    users = carregar_usuarios()
    ukey = username.lower().strip()
    ekey = email.lower().strip()
    for u in users:
        if u.get("usuario_key") == ukey and u.get("email_key") == ekey and u.get("senha") == password:
            return True
    return False

def carregar_cardapio():
    menu = {}
    if not os.path.exists(MENU_FILE):
        return menu
    with open(MENU_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 2:
                continue
            name, price_str = parts[0].strip(), parts[1].strip()
            try:
                price = float(price_str)
            except ValueError:
                continue
            menu[name.lower()] = {"name": name, "price": price}
    return menu

def buscar_alimento(menu: dict, term: str):
    term = term.lower().strip()
    results = []
    for key, item in menu.items():
        if term in key:
            results.append(item)
    def chave_nome(item):
        return item["name"]
    return sorted(results, key=chave_nome)

def carregar_pedidos():
    orders = []
    if not os.path.exists(ORDERS_FILE):
        return orders
    with open(ORDERS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) not in (5, 6):
                continue
            oid_str, username, items_str, total_str, rating_str = parts[:5]
            paid_str = parts[5] if len(parts) == 6 else "0"
            try:
                oid = int(oid_str)
                total = float(total_str)
                rating = float(rating_str) if rating_str.strip() != "" else None
                paid = True if paid_str.strip() == "1" else False
            except ValueError:
                continue
            items = {}
            items_str = items_str.strip()
            if items_str:
                for pair in items_str.split(","):
                    if not pair:
                        continue
                    if ":" not in pair:
                        continue
                    name, qty_str = pair.split(":", 1)
                    try:
                        qty = int(qty_str)
                    except ValueError:
                        continue
                    items[name] = qty
            orders.append({
                "id": oid,
                "user": username,
                "items": items,
                "total": total,
                "rating": rating,
                "paid": paid,
            })
    return orders

def salvar_pedidos(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        for o in orders:
            items_str = ",".join([f"{name}:{qty}" for name, qty in o["items"].items()])
            rating_str = str(o["rating"]) if o["rating"] is not None else ""
            paid_str = "1" if o.get("paid") else "0"
            f.write(f"{o['id']}|{o['user']}|{items_str}|{o['total']}|{rating_str}|{paid_str}\n")

def proximo_id_pedido(orders):
    if not orders:
        return 1
    return max(o["id"] for o in orders) + 1

def calcular_total(items: dict, menu: dict) -> float:
    total = 0.0
    for name, qty in items.items():
        entry = menu.get(name.lower())
        if entry:
            total += entry["price"] * qty
    return round(total, 2)

def imprimir_lista_alimentos(items):
    if not items:
        print("Nenhum alimento encontrado.")
        return
    print("Alimentos encontrados:")
    for idx, it in enumerate(items, start=1):
        print(f"{idx}) {it['name']} (R$ {it['price']:.2f})")

def pedir_inteiro(msg, allow_empty=False):
    while True:
        val = input(msg).strip()
        if allow_empty and val == "":
            return None
        try:
            return int(val)
        except ValueError:
            print("Digite um número inteiro válido.")

def pedir_float(msg, allow_empty=False):
    while True:
        val = input(msg).strip()
        if allow_empty and val == "":
            return None
        try:
            val = val.replace(",", ".")
            return float(val)
        except ValueError:
            print("Digite um número válido (pode ser decimal).")

def pedir_nao_vazio(msg, allow_empty=False):
    while True:
        val = input(msg).strip()
        if allow_empty and val == "":
            return None
        if val:
            return val
        print("O valor não pode ser vazio.")

def pedir_apenas_letras(msg, allow_empty=False):
    while True:
        val = input(msg).strip()
        if allow_empty and val == "":
            return None
        if val and all(ch.isalpha() or ch.isspace() for ch in val):
            return val
        print("Digite apenas letras (sem números ou caracteres especiais).")

def pedir_opcao_menu(valid_options, allow_empty=False):
    valid_set = {str(v) for v in valid_options}
    while True:
        val = input("Opção: ").strip()
        if allow_empty and val == "":
            return None
        if val.isdigit() and val in valid_set:
            return val
        print("Opção inválida. Digite apenas números das opções.")

def imprimir_cardapio_numerado(menu: dict):
    items = [v for v in menu.values()]
    print("\n=== Cardápio ===")
    for idx, it in enumerate(items, start=1):
        print(f"{idx}) {it['name']} - R$ {it['price']:.2f}")
    return items

def ler_lista_numeros(msg, max_index, allow_empty=False):
    while True:
        raw = input(msg).strip()
        if allow_empty and raw == "":
            return None
        if not raw:
            print("Entrada vazia. Digite números separados por vírgula ou pressione Enter para voltar.")
            continue
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        if not parts:
            print("Entrada inválida. Tente novamente.")
            continue
        if all(p.isdigit() for p in parts):
            nums = [int(p) for p in parts]
            if all(1 <= n <= max_index for n in nums):
                return nums
        print("Use apenas números válidos, separados por vírgula, conforme o cardápio.")

def ler_itens_com_quantidade(msg, max_index, allow_empty=False):
    while True:
        raw = input(msg).strip()
        if allow_empty and raw == "":
            return None
        if not raw:
            print("Entrada vazia. Digite números separados por vírgula (ex: 2,1,4) ou com quantidade (ex: 2x5,4x1).")
            continue
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        if not parts:
            print("Entrada inválida. Tente novamente.")
            continue
        result = []
        ok = True
        for p in parts:
            if any(sep in p for sep in ("x", "*", ":")):
                for sep in ("x", "*", ":"):
                    if sep in p:
                        left, right = p.split(sep, 1)
                        break
                if not left.isdigit() or not right.isdigit():
                    ok = False
                    break
                idx = int(left)
                qty = int(right)
            else:
                if not p.isdigit():
                    ok = False
                    break
                idx = int(p)
                qty = 1
            if not (1 <= idx <= max_index) or qty <= 0:
                ok = False
                break
            result.append((idx, qty))
        if ok:
            return result
        print("Use índices válidos (conforme cardápio) e quantidades >= 1. Ex: 2,1,4 ou 2x5,4x1.")

def pedir_email_valido(msg, allow_empty=False):
    while True:
        val = input(msg).strip()
        if allow_empty and val == "":
            return None
        if val == "":
            print("E-mail não pode ser vazio.")
            continue
        if "@" in val and "." in val and " " not in val:
            return val
        print("E-mail inválido. Ex: nome@dominio.com")

def fluxo_cadastrar_usuario():
    print("\n=== Cadastrar novo usuário ===")
    username = pedir_apenas_letras("Usuário (apenas letras, Enter para voltar): ", allow_empty=True)
    if username is None:
        return
    email = pedir_email_valido("E-mail (Enter para voltar): ", allow_empty=True)
    if email is None:
        return
    password = pedir_nao_vazio("Senha (qualquer caractere, Enter para voltar): ", allow_empty=True)
    if password is None:
        return
    salvar_usuario(username, password, email)
    print("Usuário cadastrado com sucesso!")

def fluxo_login_usuario():
    print("\n=== Login (nome + e-mail + senha) ===")
    username = pedir_apenas_letras("Usuário (apenas letras, Enter para voltar): ", allow_empty=True)
    if username is None:
        return None
    email = pedir_email_valido("E-mail (Enter para voltar): ", allow_empty=True)
    if email is None:
        return None
    password = pedir_nao_vazio("Senha (qualquer caractere, Enter para voltar): ", allow_empty=True)
    if password is None:
        return None
    if autenticar(username, email, password):
        print("Login realizado!")
        return username.lower().strip()
    print("Usuário/e-mail/senha inválidos ou usuário sem e-mail cadastrado.")
    return None

def fluxo_busca(menu):
    term = pedir_nao_vazio("Buscar por alimento (termo): ")
    results = buscar_alimento(menu, term)
    imprimir_lista_alimentos(results)

def listar_meus_pedidos(username, orders):
    mine = [o for o in orders if o["user"] == username]
    if not mine:
        print("Você não possui pedidos.")
        return []
    print("\n=== Meus pedidos ===")
    for i, o in enumerate(mine, start=1):
        items_desc = ", ".join([f"{name} x{qty}" for name, qty in o["items"].items()]) or "(vazio)"
        rating_desc = o["rating"] if o["rating"] is not None else "(sem avaliação)"
        paid_desc = "(pago)" if o.get("paid") else "(não pago)"
        print(f"Pedido {i} | ID {o['id']} | Itens: {items_desc} | Total: R$ {o['total']:.2f} | Avaliação: {rating_desc} {paid_desc}")
    return mine

def criar_pedido(username, orders, menu):
    oid = proximo_id_pedido(orders)
    temp_order = {"id": oid, "user": username, "items": {}, "total": 0.0, "rating": None, "paid": False}
    print(f"Pedido criado com ID {oid}.")
    items_list = imprimir_cardapio_numerado(menu)
    max_index = len(items_list)
    added_any = False
    while True:
        entries = ler_itens_com_quantidade(
            "Digite os itens por número (ex: 2,1,4) ou com quantidade (ex: 2x20,4x3). Enter para voltar: ",
            max_index,
            allow_empty=True,
        )
        if entries is None:
            break
        for idx, qty in entries:
            item_name = items_list[idx - 1]["name"]
            temp_order["items"][item_name] = temp_order["items"].get(item_name, 0) + qty
            added_any = True
        temp_order["total"] = calcular_total(temp_order["items"], menu)
        print(f"Itens atuais: {', '.join([f'{n} x{q}' for n, q in temp_order['items'].items()])} | Total: R$ {temp_order['total']:.2f}")
        cont = input("Deseja continuar adicionando itens? (s/n, Enter para sair): ").strip().lower()
        if cont == "" or cont == "n":
            break
        elif cont != "s":
            print("Resposta inválida. Use 's', 'n' ou Enter.")
    if not added_any:
        print("Pedido cancelado. Voltando.")
        return
    orders.append(temp_order)
    salvar_pedidos(orders)
    print("Pedido finalizado (você pode editar depois).")

def editar_itens_pedido(username, orders, menu):
    mine = listar_meus_pedidos(username, orders)
    if not mine:
        return
    idx = pedir_inteiro("Editar qual pedido (número da lista, Enter para voltar): ", allow_empty=True)
    if idx is None:
        return
    if idx < 1 or idx > len(mine):
        print("Pedido inválido.")
        return
    order = mine[idx - 1]
    while True:
        print("\n1) Adicionar itens (lista, ex: 2,1,4 ou 2x5,4x1)\n2) Remover quantidades de itens (lista, ex: 2,1,4 ou 2x3)\n3) Voltar")
        opt = pedir_opcao_menu([1, 2, 3], allow_empty=True)
        if opt is None:
            break
        items_list = imprimir_cardapio_numerado(menu)
        max_index = len(items_list)
        if opt == "1":
            entries = ler_itens_com_quantidade(
                "Itens para adicionar (ex: 2,1,4 ou 2x5,4x1). Enter para voltar: ",
                max_index,
                allow_empty=True,
            )
            if entries is None:
                pass
            else:
                for idx, qty in entries:
                    item_name = items_list[idx - 1]["name"]
                    order["items"][item_name] = order["items"].get(item_name, 0) + qty
        elif opt == "2":
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
                    if item_name in order["items"]:
                        current = order["items"].get(item_name, 0)
                        new_qty = current - qty
                        if new_qty <= 0:
                            del order["items"][item_name]
                        else:
                            order["items"][item_name] = new_qty
                    else:
                        print(f"Item '{item_name}' não está no pedido.")
        elif opt == "3":
            break
        order["total"] = calcular_total(order["items"], menu)
        itens_str = ", ".join([f"{n} x{q}" for n, q in order["items"].items()]) or "(vazio)"
        print(f"Itens atuais: {itens_str} | Total: R$ {order['total']:.2f}")
    salvar_pedidos(orders)
    print("Pedido atualizado.")

def excluir_pedido(username, orders):
    mine = listar_meus_pedidos(username, orders)
    if not mine:
        return
    idx = pedir_inteiro("Excluir qual pedido (número da lista, Enter para voltar): ", allow_empty=True)
    if idx is None:
        return
    if idx < 1 or idx > len(mine):
        print("Pedido inválido.")
        return
    order = mine[idx - 1]
    confirm = input("Continuar? (s/n): ").strip().lower()
    if confirm == "s":
        orders.remove(order)
        salvar_pedidos(orders)
        print("Pedido excluído.")
    else:
        print("Exclusão cancelada.")

def avaliar_pedido(username, orders):
    mine = listar_meus_pedidos(username, orders)
    if not mine:
        return
    idx = pedir_inteiro("Avaliar qual pedido (número da lista, Enter para voltar): ", allow_empty=True)
    if idx is None:
        return
    if idx < 1 or idx > len(mine):
        print("Pedido inválido.")
        return
    order = mine[idx - 1]
    rating = pedir_float("Nota (0 a 5, pode ser decimal; vazio para remover): ", allow_empty=True)
    if rating is None:
        order["rating"] = None
    elif 0 <= rating <= 5:
        order["rating"] = rating
    else:
        print("Nota inválida.")
        return
    salvar_pedidos(orders)
    print("Avaliação registrada.")

def pagar_pedido(username, orders):
    mine = listar_meus_pedidos(username, orders)
    if not mine:
        return
    idx = pedir_inteiro("Pagar qual pedido (número da lista, Enter para voltar): ", allow_empty=True)
    if idx is None:
        return
    if idx < 1 or idx > len(mine):
        print("Pedido inválido.")
        return
    order = mine[idx - 1]
    if not order["items"]:
        print("Pedido vazio, adicione itens antes de pagar.")
        return
    if order.get("paid"):
        print("Este pedido já está pago.")
        return
    print(f"Total a pagar: R$ {order['total']:.2f}")
    print("1) PIX\n2) Cartão\n3) Dinheiro\n(Enter para voltar)")
    opt = pedir_opcao_menu([1, 2, 3], allow_empty=True)
    if opt is None:
        print("Pagamento cancelado.")
        return
    elif opt == "1":
        print("Chave PIX: feifood@exemplo.com")
    elif opt == "2":
        print("Pagamento no cartão processado")
    elif opt == "3":
        print("Pagamento em dinheiro registrado")
    confirmar = input("Confirmar pagamento? (s/n, Enter para voltar): ").strip().lower()
    if confirmar == "":
        print("Pagamento cancelado.")
        return
    if confirmar != "s":
        print("Pagamento não confirmado.")
        return
    order["paid"] = True
    salvar_pedidos(orders)
    print("Pagamento concluído.")

def menu_pedidos(username, menu):
    while True:
        orders = carregar_pedidos()
        print("\n=== Pedidos ===")
        print("1) Criar pedido")
        print("2) Editar itens do pedido")
        print("3) Excluir pedido")
        print("4) Listar meus pedidos")
        print("5) Avaliar pedido")
        print("6) Pagar pedido")
        print("7) Voltar (Enter também volta)")
        opt = pedir_opcao_menu([1, 2, 3, 4, 5, 6, 7], allow_empty=True)
        if opt is None:
            return
        if opt == "1":
            criar_pedido(username, orders, menu)
        elif opt == "2":
            editar_itens_pedido(username, orders, menu)
        elif opt == "3":
            excluir_pedido(username, orders)
        elif opt == "4":
            listar_meus_pedidos(username, orders)
        elif opt == "5":
            avaliar_pedido(username, orders)
        elif opt == "6":
            pagar_pedido(username, orders)
        elif opt == "7":
            return

def menu_principal():
    garantir_arquivos_de_dados()
    menu = carregar_cardapio()
    logged_user = None
    while True:
        print("\n=== FEIFood ===")
        if not logged_user:
            print("1) Cadastrar novo usuário")
            print("2) Login")
            print("3) Sair")
            opt = pedir_opcao_menu([1, 2, 3])
            if opt == "1":
                fluxo_cadastrar_usuario()
            elif opt == "2":
                logged_user = fluxo_login_usuario()
            elif opt == "3":
                print("Encerrando...")
                break
        else:
            print(f"Usuário logado: {logged_user}")
            print("1) Listar cardápio completo")
            print("2) Buscar por alimento")
            print("3) Gerenciar pedidos")
            print("4) Logout")
            print("0) Sair")
            opt = pedir_opcao_menu([0, 1, 2, 3, 4])
            if opt == "1":
                menu = carregar_cardapio()
                imprimir_cardapio_numerado(menu)
            elif opt == "2":
                menu = carregar_cardapio()
                fluxo_busca(menu)
            elif opt == "3":
                menu = carregar_cardapio()
                menu_pedidos(logged_user, menu)
            elif opt == "4":
                logged_user = None
                print("Logout realizado.")
            elif opt == "0":
                print("Encerrando...")
                break

if __name__ == "__main__":
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\nEncerrado.")
        sys.exit(0)
