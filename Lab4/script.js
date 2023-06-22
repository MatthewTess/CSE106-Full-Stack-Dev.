class Calculator {
  constructor(previousOperandTextElement, currentOperandTextElement) {
    this.previousOperandTextElement = previousOperandTextElement;
    this.currentOperandTextElement = currentOperandTextElement;
    this.clear();
    this.clicked = false;
    this.previousCurrent = null;
    this.clickCount = 0;
  }

  setClicked(){
    if(this.clickCount == 2){
      this.clicked = true;
    }else if(this.clickCount == 0){
      this.clickCount = 1;
    }else if(this.clickCount == 1){
      this.clickCount = 2;
    }
    
  }

  unclick(){
    this.clicked = false;
    this.clickCount = 0;
  }


  clear() {
    this.currentOperand = "";
    this.previousOperand = "";
    this.operation = undefined;
    this.answer = null;
  }

  appendNumber(number) {
    this.unclick();
    if (number === '.' && this.currentOperand.includes('.')) return
    this.currentOperand = this.currentOperand.toString() + number.toString()
  }

  chooseOperation(operation) {
    console.log(this.clicked);
    if (this.clicked) {
      this.previousOperand = this.answer;
      this.operation = operation
      this.currentOperand = ''
      this.updateDisplay();
      this.unclick();
      return;
    }else if(this.clickCount == 1){
      this.previousOperand = this.answer;
      this.operation = operation
      this.currentOperand = ''
      this.updateDisplay();
      this.unclick();
      return;
    }
    this.unclick();
    if (this.currentOperand === '') return
    if (this.previousOperand !== '') {
      this.compute()
    }
    this.operation = operation
    this.previousOperand = this.currentOperand
    this.currentOperand = ''
  }

  compute() {
    if (this.clicked) {
      this.previousOperand = this.currentOperand;
      this.currentOperand = this.previousCurrent;
      this.updateDisplay();
    }
    let computation;
    const prev = parseFloat(this.previousOperand);
    const current = parseFloat(this.currentOperand);
    if (isNaN(prev) || isNaN(current)) return;
    switch (this.operation) {
      case "+":
        computation = prev + current;
        break;
      case "-":
        computation = prev - current;
        break;
      case "*":
        computation = prev * current;
        break;
      case "/":
        computation = prev / current;
        break;
      default:
        return;
    }
    if (!this.clicked) {
      this.previousCurrent = this.currentOperand
    }
    this.currentOperand = computation;
    if (this.answer != null) {
      this.previousOperand = this.answer;
    } else {
      this.previousOperand = prev;
    }
    this.answer = computation;
  }


  getDisplayNumber(number) {
    const stringNumber = number.toString()
    const integerDigits = parseFloat(stringNumber.split('.')[0])
    const decimalDigits = stringNumber.split('.')[1]
    let integerDisplay
    if (isNaN(integerDigits)) {
      integerDisplay = ''
    } else {
      integerDisplay = integerDigits.toLocaleString('en', { maximumFractionDigits: 0 })
    }
    if (decimalDigits != null) {
      return `${integerDisplay}.${decimalDigits}`
    } else {
      return integerDisplay
    }
  }

  updateDisplay() {
    this.currentOperandTextElement.innerText =
      this.getDisplayNumber(this.currentOperand)
    if (this.operation != null) {
      this.previousOperandTextElement.innerText =
        `${this.getDisplayNumber(this.previousOperand)} ${this.operation}`
    } else {
      this.previousOperandTextElement.innerText = ''
    }
  }
}


const numberButtons = document.querySelectorAll('[data-number]')
const operationButtons = document.querySelectorAll('[data-operation]')
const equalsButton = document.querySelector('[data-equals]')
const allClearButton = document.querySelector('[data-all-clear]')
const previousOperandTextElement = document.querySelector('[data-previous-operand]')
const currentOperandTextElement = document.querySelector('[data-current-operand]')
let activeButton = null;
const calculator = new Calculator(previousOperandTextElement, currentOperandTextElement)

function removeHighlight() {
  operationButtons.forEach(btn => {
    btn.classList.remove("active");
    btn.style.backgroundColor = "#61a055";
  });
}


numberButtons.forEach(button => {
  button.addEventListener('click', () => {
    calculator.appendNumber(button.innerText)
    calculator.updateDisplay()
    removeHighlight();
  })
})

operationButtons.forEach(button => {
  button.addEventListener('click', () => {
    calculator.chooseOperation(button.attributes.getNamedItem("value").value)
    calculator.updateDisplay()
  })
})

equalsButton.addEventListener('click', button => {
  calculator.setClicked();
  calculator.compute()
  calculator.updateDisplay()
  removeHighlight();
})

allClearButton.addEventListener('click', button => {
  calculator.clear()
  calculator.updateDisplay()
  removeHighlight();
})


operationButtons.forEach(button => {
  button.addEventListener("click", () => {
    // Remove active class from all buttons
    removeHighlight();

    // Add active class to clicked button
    button.classList.toggle("active");
    // Change background color to blue
    button.style.backgroundColor = "blue";
    // Handle button click logic
    // ...
  });
});


allClearButton.forEach(button => {
  button.addEventListener("click", () => {
    removeHighlight();
    button.style.backgroundColor = "blue";
    // Set clicked button as active
    activeButton = button;
  });
});






