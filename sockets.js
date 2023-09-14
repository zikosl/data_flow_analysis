exports.Sockets = async (socket,io)=>{
    socket.on('storeClientInfo', async (data) => {
        socket.customId = data.customId;
        
    });
    socket.on("disconnect", () => {
    })
} 