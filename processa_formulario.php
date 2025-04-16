<?php
// Configurações do banco de dados
$host = 'localhost';
$dbname = 'fernanda_imoveis';
$user = 'root';
$password = '';

// Conexão com o banco de dados
try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $user, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    die("Erro na conexão com o banco de dados: " . $e->getMessage());
}

// Verifica se o formulário foi enviado
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Verifica qual formulário foi enviado
    if (isset($_POST['formulario_contato'])) {
        // Dados do formulário de contato
        $nome = $_POST['nome'] ?? '';
        $email = $_POST['email'] ?? '';
        $telefone = $_POST['telefone'] ?? '';
        $mensagem = $_POST['mensagem'] ?? '';

        // Validação do número de telefone
        if (!preg_match('/^\d{2} - 9\d{4}-\d{4}$|^\d{11}$/', $telefone)) {
            echo "<script>alert('Por favor, insira um número de celular válido no formato xx - 9xxxx-xxxx ou xxxxxxxxxxx.'); window.location.href = '/Landing_Page/index.html';</script>";
            exit;
        }

        // Validação básica
        if (!empty($nome) && !empty($email) && !empty($telefone) && !empty($mensagem)) {
            // Insere os dados no banco de dados
            $sql = "INSERT INTO formulario_contato (nome, email, telefone, mensagem) VALUES (:nome, :email, :telefone, :mensagem)";
            $stmt = $pdo->prepare($sql);
            $stmt->execute([
                ':nome' => $nome,
                ':email' => $email,
                ':telefone' => $telefone,
                ':mensagem' => $mensagem,
            ]);
            // Exibe mensagem de sucesso e recarrega a página
            echo "<script>alert('Cadastro realizado com sucesso!'); window.location.href = '/Landing_Page/index.html';</script>";
            exit;
        } else {
            echo "<script>alert('Por favor, preencha todos os campos.');</script>";
        }
    } elseif (isset($_POST['formulario_whatsapp'])) {
        // Dados do formulário de WhatsApp
        $telefone = $_POST['telefone'] ?? '';

        // Validação do número de telefone
        if (!preg_match('/^\d{2} - 9\d{4}-\d{4}$|^\d{11}$/', $telefone)) {
            echo "<script>alert('Por favor, insira um número de celular válido no formato xx - 9xxxx-xxxx ou xxxxxxxxxxx.'); window.location.href = '/Landing_Page/index.html';</script>";
            exit;
        }

        // Validação básica
        if (!empty($telefone)) {
            // Insere os dados no banco de dados
            $sql = "INSERT INTO formulario_whatsapp (telefone) VALUES (:telefone)";
            $stmt = $pdo->prepare($sql);
            $stmt->execute([
                ':telefone' => $telefone,
            ]);
            // Exibe mensagem de sucesso e recarrega a página
            echo "<script>alert('Cadastro realizado com sucesso!'); window.location.href = '/Landing_Page/index.html';</script>";
            exit;
        } else {
            echo "<script>alert('Por favor, preencha o campo de telefone.');</script>";
        }
    }
}
