## Nosso exemplo de aggregate 
<br><br>
<img src="aggregate.png">
<br><br>
db.Requerentes.aggregate([<br>
  {<br>
    $match: {<br>
      _id: ObjectId("ID_EXEMPLO") <br>
    }<br>
  },<br>
  {<br>
    $lookup: {<br>
      from: "Produtos", <br>
      localField: "alimento",<br>
      foreignField: "nome",<br>
      as: "produto"<br>
    }<br>
  },<br>
  {<br>
    $unwind: "$produto"
  },
  {
    $set: {
      "produto.nome": "Feijão" 
    }
  },
  {<br>
    $merge: {
      into: "Requerentes", 
      whenMatched: "merge", 
      whenNotMatched: "insert" 
    }
  }
]);


