import telebot

<?php

// ====== CONFIG ======
$BOT_TOKEN = "8763718986:AAFaVGHQe-QiG1waO24-ZH5jY4-t9FcRWnA";
$ADMIN_CHAT_ID = "7591567094:AAF1buYRC6-Rz00FLDwSJ_6cnF299fML84k"; // lead keladigan joy
$OPENAI_API_KEY = "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";

// ====== UPDATE ======
$update = json_decode(file_get_contents("php://input"), TRUE);
$message = $update["message"]["text"] ?? "";
$chat_id = $update["message"]["chat"]["id"] ?? "";
$name = $update["message"]["from"]["first_name"] ?? "";

// ====== SEND FUNCTION ======
function sendMessage($chat_id, $text){
    global $BOT_TOKEN;
    file_get_contents("https://api.telegram.org/bot$BOT_TOKEN/sendMessage?chat_id=$chat_id&text=".urlencode($text));
}

// ====== AI FUNCTION ======
function askAI($text){
    global $OPENAI_API_KEY;

    $data = [
        "model" => "gpt-4.1-mini",
        "messages" => [
            [
                "role" => "system",
                "content" => "You are TOGO GROUP PRO AI sales bot. 
Respond in user's language. 
You calculate prices:
- 3D letters: 9000 so'm per cm
- Banner: 35000 so'm per m2
- Lightbox: 1500000 so'm per m2
- Vizitka: 100 dona = 80000 so'm
Ask minimal questions. Sell and close."
            ],
            ["role" => "user", "content" => $text]
        ]
    ];

    $ch = curl_init("https://api.openai.com/v1/chat/completions");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Content-Type: application/json",
        "Authorization: Bearer $OPENAI_API_KEY"
    ]);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));

    $response = curl_exec($ch);
    $res = json_decode($response, true);

    return $res["choices"][0]["message"]["content"] ?? "Xatolik";
}

// ====== PRICE LOGIC (manual) ======
function calculatePrice($text){
    $text = strtolower($text);

    // abyomni bukva
    if(preg_match('/(\d+)\s*sm/', $text, $h) && preg_match('/(\d+)\s*ta/', $text, $c)){
        $height = intval($h[1]);
        $count = intval($c[1]);
        $price = $height * 9000 * $count;
        return "💡 Hisob:\n$height sm × $count ta = ".number_format($price,0," "," ")." so‘m";
    }

    // banner
    if(preg_match('/(\d+)\s*x\s*(\d+)/', $text, $m)){
        $m2 = $m[1] * $m[2];
        $price = $m2 * 35000;
        return "🟨 Banner:\n$m2 m² = ".number_format($price,0," "," ")." so‘m";
    }

    // vizitka
    if(strpos($text, "vizitka") !== false){
        return "📊 100 dona vizitka = 80 000 so‘m\nNechta kerak?";
    }

    return null;
}

// ====== MAIN ======

if($message){

    // salomlashish
    if($message == "/start"){
        sendMessage($chat_id, "Assalomu alaykum! TOGO GROUP PRO 🤖\nQanday reklama kerak?");
        exit;
    }

    // avval hisoblashga harakat
    $calc = calculatePrice($message);

    if($calc){
        sendMessage($chat_id, $calc);
    } else {
        // AI javob
        $ai = askAI($message);
        sendMessage($chat_id, $ai);
    }

    // ===== LEAD =====
    if(preg_match('/\+?\d{9,13}/', $message, $phone)){
        $lead = "🔥 YANGI LEAD\nIsm: $name\nRaqam: ".$phone[0]."\nXabar: $message";
        sendMessage($ADMIN_CHAT_ID, $lead);

        sendMessage($chat_id, "✅ Raqamingiz qabul qilindi! Tez orada bog‘lanamiz.");
    }
}

?>
