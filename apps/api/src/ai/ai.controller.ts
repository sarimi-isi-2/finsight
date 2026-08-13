import {
  Body,
  Controller,
  Post,
  BadRequestException,
} from '@nestjs/common';

import { AiService } from './ai.service';

@Controller('ai')
export class AiController {
  constructor(
    private readonly aiService: AiService,
  ) {}

  @Post('predict')
  async predict(
    @Body('text') text: string,
  ) {
    if (!text || !text.trim()) {
      throw new BadRequestException(
        'text wajib diisi',
      );
    }

    return this.aiService.predictTransaction(text);
  }
}