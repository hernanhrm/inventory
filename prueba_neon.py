import psycopg2

DATABASE_URL = "postgresql://neondb_owner:npg_XU64qTHGkbSF@ep-withered-mountain-amxs3aij-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # 1. Insertar un producto de prueba
    # Usamos %s por seguridad (evita ataques de inyección SQL)
    nombre_prod = "Laptop Gamer"
    precio_prod = 1200.50
    cantidad_prod = 5

    cur.execute("""
        INSERT INTO productos (nombre, precio, cantidad) 
        VALUES (%s, %s, %s);
    """, (nombre_prod, precio_prod, cantidad_prod))

    # ¡IMPORTANTE! En operaciones de escritura (INSERT, UPDATE, DELETE), 
    # siempre hay que hacer commit para que los cambios se guarden.
    conn.commit()
    print(f"Producto '{nombre_prod}' insertado con éxito.")

    # 2. Consultar la tabla para ver qué hay guardado
    cur.execute("SELECT * FROM productos;")
    filas = cur.fetchall()

    print("\n--- Inventario Actual ---")
    for fila in filas:
        print(f"ID: {fila[0]} | Nombre: {fila[1]} | Precio: ${fila[2]} | Stock: {fila[3]}")

    cur.close()
    conn.close()

except Exception as e:
    print(f"Hubo un error: {e}")