var i = 1;
// some code
i = i + ""; // oops!
// some more code 

console.log("i+1", i + 1); // evaluates to the String '11'
console.log("i-1", i - 1); // evaluates to the Number 0


var j = "1";
j++; // j becomes 2
console.log('j++', j);

var k = "1";
k += 1; // k becomes "11"
console.log('k+=1', k);

l = [1, 5, 20, 10].sort() // [1, 10, 20, 5]
console.log('[1,5,20,10].sort()', l);

// lines (expressions) are terminated by a ; right?
function f1() {
  return { a: 5 };
}
function f2() {
  return {
    a: 5
  };
}
function f3() {
  return // doesn't go to the ; just returns undefined
  {
    a: 5
  };
}
console.log('return on one line: ', f1()); // {a:5}
console.log('return on multiple lines: ', f2()); // {a:5}
console.log('return on multiple lines: ', f3()); // undefined

// PROBLEMS / INCORRECT BEHAVIOR, BUT NOT JS FAULT:
console.log('0.1 + 0.2 =', 0.1 + 0.2); // 0.30000000000000004
// Not just a JS problem, a decimal to binary problem

// NaN is a special value meaning "Not A Number"
console.log('typeof NaN = ', typeof NaN); // Not-A-Number is a number
// but Python does this too type(float('nan'))==<class 'float'>


// And for fairness,
// Why JS is great: fast simple available in every browser

