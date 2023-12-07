
Nosso exemplo de aggregate 

db.Requerentes.aggregate([
  {
    $match: {
      _id: ObjectId("656f179c02210e1a1af60331") // Filtre pelo ID desejado
    }
  },
  {
    $lookup: {
      from: "Produtos", // Nome da coleção a ser unida
      localField: "alimento",
      foreignField: "nome",
      as: "produto"
    }
  },
  {
    $unwind: "$produto" // Desconstrua o array resultante do $lookup
  },
  {
    $set: {
      "produto.nome": "Feijão" // Atualize o campo "nome" no documento unido
    }
  },
  {
    $merge: {
      into: "Requerentes", // Coleção de destino para a mesclagem
      whenMatched: "merge", // Ação a ser realizada quando houver correspondência
      whenNotMatched: "insert" // Ação a ser realizada quando não houver correspondência
    }
  }
]);


