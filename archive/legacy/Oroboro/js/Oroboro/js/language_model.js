class LanguageModel {


interpret(input){

let tokens =
input.toLowerCase()
.split(" ");


return {

raw:input,

tokens:tokens,

meaning:
this.findMeaning(tokens)

};

}



findMeaning(tokens){


if(tokens.includes("explore"))
return "DISCOVERY";


if(tokens.includes("find"))
return "SEARCH";


if(tokens.includes("remember"))
return "MEMORY";


return "UNKNOWN";


}


}


window.Language =
new LanguageModel();