FROM node:20-slim
WORKDIR /app
COPY . .
EXPOSE 7860
ENV PORT=7860
CMD ["node", "bot.mjs"]
