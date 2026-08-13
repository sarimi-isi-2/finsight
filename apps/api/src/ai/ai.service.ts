import {
  Injectable,
  HttpException,
  HttpStatus,
} from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class AiService {
  constructor(
    private readonly configService: ConfigService,
  ) {}

  async predictTransaction(text: string) {
    try {
      const aiServiceUrl =
        this.configService.get<string>(
          'AI_SERVICE_URL',
        ) || 'http://127.0.0.1:5000';

      const response = await fetch(
        `${aiServiceUrl}/api/v1/predict`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            text,
          }),
        },
      );

      if (!response.ok) {
        throw new Error(
          `AI service returned ${response.status}`,
        );
      }

      return await response.json();
    } catch (error) {
      throw new HttpException(
        {
          message:
            'AI service tidak dapat diakses',
          error: String(error),
        },
        HttpStatus.BAD_GATEWAY,
      );
    }
  }
}