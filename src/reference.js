var rollDice = (dices,sides) => 
    { 
        if (dices == 0){dices = 1;}
        if (sides == 0){return null;}
    
        var roll = [];
        
        for (i = 0; i < dices; i++)
        {                
            var randomNumber = Math.floor(Math.random() * sides) + 1;
            roll.push(randomNumber);                
        }
        
        roll.sort(function(a, b){return b-a});
    
        let results = [roll, arreySum(roll)];
    
        return results;
    }
    
    var arreySum = (currentArrey) => 
    {
        let total = 0;
        for (s in currentArrey) {total = total + currentArrey[s];}
        return total;
    }
    
    var arreyTrim = (freeDiceArray, position, number) => 
    {    
        if (freeDiceArray.length == 0 ){return null;}
    
        let copyArrey = freeDiceArray[freeDiceArray.length -1].slice();    
    
        if (position == 'l') {copyArrey.sort(function(a, b){return a-b});}  
        let trimArray = copyArrey.slice(0, number);
    
        trimArray.sort(function(a, b){return b-a});
        
        let results = [trimArray, arreySum(trimArray)];
        
        return results;    
    }
    
    var commandHandler = (input) => 
    { 
        input = input.substring('/r'.length).trim();
    
        if (!input || input.includes("d") == false) {return null;}
    
        // Separa os elementos do comando
        const parameters = input.match(/(\d*)d(\d+)|([+-])|[hl]|(\d+)/g);
        
        console.log('Paramentros iniciais: '+parameters);
      
        let freeDiceArray = [];
        let keptDiceArray = [];
        let partialValue = 0;
        let totalValue = 0;    
        let signal = 1;
        let presentation = '';    
    
        for (p = 0; p < parameters.length; p++)
        {
            if (parameters[p].includes("d") == true) //testa se é um dado 
                {
                    let values = parameters[p].split("d");                              // Divide os parametros
                    let roll = rollDice(Number(values[0]) ,Number(values[1]) );         // Rola os dados e soma                                                         
                    partialValue = partialValue + roll[1];                              // Adiciona ao parcial 
                    freeDiceArray.push(roll[0]);                                            // Registra para apresentação                        
                }
    
            if (parameters[p] == 'l' || parameters[p] == 'h')                           // testa lower ou highter  
                {                           
                    let trimArray = arreyTrim(freeDiceArray,parameters[p],parameters[p+1]); // Gera sub array              
                    partialValue = trimArray[1];                                        //console.log('tempArray: '+trimArray);
                    keptDiceArray.push(trimArray[0])
                    
                }
            if (parameters[p] == '+' || parameters[p] == '-')   
                {
                    if (parameters[p+1].includes("d") == true) 
                    {
                      totalValue = totalValue + (signal * partialValue); 
                      partialValue = 0;
                      signal = Number(parameters[p]+'1');               
                    }
                    else {partialValue = partialValue + Number(parameters[p]+parameters[p+1]);} 
                }
        }
    
        totalValue = totalValue + (signal * partialValue); 
            
        if   (keptDiceArray.length == 0 )        {presentation = 'Roll: '+input+'\nResults: '+freeDiceArray+'\nTotal: ' + totalValue;}    
        else {presentation = 'Roll: '+input+'\nResults: '+freeDiceArray+', values kept: '+keptDiceArray+','+'\nTotal: ' + totalValue;}
        
        //console.log('Array de dados: ' + freeDiceArray);
        //console.log(presentation);
    
        return presentation;
    }