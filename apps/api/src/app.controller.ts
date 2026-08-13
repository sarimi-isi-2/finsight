import { Body, Controller, Get, Post } from '@nestjs/common';
import { AppService } from './app.service';
import { AiService } from './ai/ai.service';

@Controller()
export class AppController {
  constructor(
    private readonly appService: AppService,
    private readonly aiService: AiService,
  ) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }

  @Post('ai/predict')
  async predictTransaction(
    @Body() body: { text: string },
  ) {
    return this.aiService.predictTransaction(body.text);
  }
}