var i = 1;
// i = the integer 1
i = i + "";
// i now = the STRING 1?!
console.log("i+1", i + 1); // evaluates to the String '11'
console.log("i-1", i - 1); // evaluates to the Number 0
i++; // i is now the integer 2
console.log('i++', i); // evaluates to the integer 2

i=1; // int 1
i=i+""; // string 1
i+=1; // string "11" ?!
console.log('i+=1', i);

l = [1, 5, 20, 10].sort() // [1, 10, 20, 5] sorts integers alphabetically?! 
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

// == is so broken, they just abandoned the == operator and added a new operator === that doesn't do type conversions
[] == ![]   // true  (unexpected: empty array is equal to its own negation)
[] == ""    // true (unexpected: empty array coerces to empty string)
[1,2] == "1,2"  // true (array coerces to its joined string)

// function declarations are so broken, they just abandoned the "function" keyword and assign anonymous lambdas to a variable
// Using a plain function (wrong `this` binding)
function Counter() {
  this.count = 0;
  setInterval(function() {
    this.count++;
    console.log(this.count); // NaN (because `this` is the global object, not the Counter instance)
  }, 1000);
}
new Counter();

// Using an anonymous arrow function (lexical `this`)
const CounterFixed = function() {
  this.count = 0;
  setInterval(() => {
    this.count++;
    console.log(this.count); // 1, 2, 3, … as expected
  }, 1000);
};
new CounterFixed();

// PROBLEMS / INCORRECT BEHAVIOR, BUT NOT JS FAULT:
console.log('0.1 + 0.2 =', 0.1 + 0.2); // 0.30000000000000004
// Not just a JS problem, a decimal to binary problem

// NaN is a special value meaning "Not A Number"
console.log('typeof NaN = ', typeof NaN); // Not-A-Number is a number
// but Python does this too type(float('nan'))==<class 'float'>


// And for fairness,
// Why JS is great: fast simple available in every browser, async everywhere

