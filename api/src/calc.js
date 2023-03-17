export default calc = (num1, num2, op) => {
    switch(op) {
        case 'sum': return num1 + num2;
        case 'sub': return num1 - num2;
        case 'mult': return num1 * num2;
        case 'div': return num1 / num2;
    }
}