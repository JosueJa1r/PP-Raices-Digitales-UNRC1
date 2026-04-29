graph TD
    %% Estilos de los nodos
    classDef front fill:#3b82f6,stroke:#1e40af,stroke-width:2px,color:#fff;
    classDef back fill:#10b981,stroke:#047857,stroke-width:2px,color:#fff;
    classDef db fill:#f59e0b,stroke:#b45309,stroke-width:2px,color:#fff;

    %% Nodos Frontend
    Inicio([index.html - Portal Principal]) ::: front
    Portal(Selección de Perfil) ::: front

    %% Frontend: Productor
    FormProdLogin[Formulario Login Productor] ::: front
    FormProdReg[Formulario Registro Productor] ::: front
    DashProd([vistas/agricola/productor_dashboard.html]) ::: front

    %% Frontend: Cliente
    FormCliLogin[Formulario Login Cliente] ::: front
    FormCliReg[Formulario Registro Cliente] ::: front
    TiendaCli([vistas/Usuario/cliente_tienda.html]) ::: front

    %% Nodos Backend (Implementación requerida)
    API_LoginProd{{BACK: POST /api/login/productor}} ::: back
    API_RegProd{{BACK: POST /api/register/productor}} ::: back
    API_LoginCli{{BACK: POST /api/login/cliente}} ::: back
    API_RegCli{{BACK: POST /api/register/cliente}} ::: back

    %% Nodos Database (Implementación requerida)
    DB_Productores[(DBA: Tabla 'Productores')] ::: db
    DB_Clientes[(DBA: Tabla 'Clientes')] ::: db

    %% Flujo Principal
    Inicio --> Portal
    Portal -- "Soy Productor" --> FormProdLogin
    Portal -- "Soy Productor (Nuevo)" --> FormProdReg
    Portal -- "Soy Cliente" --> FormCliLogin
    Portal -- "Soy Cliente (Nuevo)" --> FormCliReg

    %% Flujo Productor con BACK y DBA
    FormProdLogin -- "Submit Credenciales" --> API_LoginProd
    FormProdReg -- "Submit Datos" --> API_RegProd
    
    API_LoginProd -. "Valida credenciales" .-> DB_Productores
    API_RegProd -. "Inserta nuevo Productor" .-> DB_Productores

    API_LoginProd -- "Éxito (Sesión/JWT)" --> DashProd
    API_RegProd -- "Éxito (Redirección)" --> DashProd

    %% Flujo Cliente con BACK y DBA
    FormCliLogin -- "Submit Credenciales" --> API_LoginCli
    FormCliReg -- "Submit Datos" --> API_RegCli

    API_LoginCli -. "Valida credenciales" .-> DB_Clientes
    API_RegCli -. "Inserta nuevo Cliente" .-> DB_Clientes

    API_LoginCli -- "Éxito (Sesión/JWT)" --> TiendaCli
    API_RegCli -- "Éxito (Redirección)" --> TiendaCli