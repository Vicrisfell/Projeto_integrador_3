
Nosso exemplo de aggregate 

db.Requerentes.aggregate([
  {
    $match: {
      _id: ObjectId("656f179c02210e1a1af60331") 
    }
  },
  {
    $lookup: {
      from: "Produtos", 
      localField: "alimento",
      foreignField: "nome",
      as: "produto"
    }
  },
  {
    $unwind: "$produto"
  },
  {
    $set: {
      "produto.nome": "Feijão" 
    }
  },
  {
    $merge: {
      into: "Requerentes", 
      whenMatched: "merge", 
      whenNotMatched: "insert" 
    }
  }
]);


