<?php
function map_range($value, $low1, $high1, $low2, $high2) {
    return $low2 + ($value - $low1) * ($high2 - $low2) / ($high1 - $low1);
}
for ($x = 1; $x <= 200000; $x++) {
    // asin(x)와 acos(x)의 입력 범위는 [-1, 1]입니다.
    $t = map_range($x, 1, 200000, -1, 1);
    if ($t < -1 || $t > 1) {
        continue;
    }

    $arcsin_x = asin($t);
    $arccos_x = acos($t);
    $arctan_x = atan($t);

    $result = $arcsin_x * $arccos_x * $arctan_x;
}
echo "OK!\n";
?>