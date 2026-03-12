import React, { useState, useRef, useEffect } from 'react';
import { Card, Input, Button, Typography, Space, Spin, Modal, Form, Select, InputNumber, message, Tag } from 'antd';
import { SendOutlined, RobotOutlined, UserOutlined, SettingOutlined, ApiOutlined, CheckCircleOutlined, CloseCircleOutlined } from '@ant-design/icons';
import { apiClient } from '../api/client';
import type { AIConfig } from '../types';
import styles from './AIAssistant.module.css';

const { Text } = Typography;

interface ChatMessage {
  id: string;
  role: 'user' | 'ai';
  content: string;
  suggestions?: string[];
}

const AIAssistant: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '0',
      role: 'ai',
      content: '你好！我是你的农场AI助手。有什么可以帮助你的吗？',
      suggestions: ['现在种什么最赚钱？', '我的农场怎么样？', '给我一些种植建议'],
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [settingsVisible, setSettingsVisible] = useState(false);
  const [aiConfig, setAiConfig] = useState<AIConfig | null>(null);
  const [configLoading, setConfigLoading] = useState(false);
  const [testingConnection, setTestingConnection] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [form] = Form.useForm();

  useEffect(() => {
    loadAIConfig();
  }, []);

  const loadAIConfig = async () => {
    try {
      const config = await apiClient.getAIConfig();
      setAiConfig(config);
    } catch (error) {
      console.error('加载AI配置失败:', error);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || loading) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await apiClient.chatWithAI(userMessage.content);
      const aiMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'ai',
        content: response.response,
        suggestions: response.suggestions,
      };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        role: 'ai',
        content: '抱歉，我遇到了一些问题。请稍后重试。',
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
  };

  const handleSaveConfig = async (values: any) => {
    setConfigLoading(true);
    try {
      const result = await apiClient.setAIConfig(values);
      if (result.success) {
        message.success(result.message);
        setAiConfig(result.config);
        setSettingsVisible(false);
      }
    } catch (error) {
      message.error('保存配置失败');
    } finally {
      setConfigLoading(false);
    }
  };

  const handleTestConnection = async () => {
    const values = form.getFieldsValue(['api_key', 'model', 'base_url', 'temperature']);
    if (!values.api_key) {
      message.warning('请先输入API密钥');
      return;
    }
    setTestingConnection(true);
    try {
      const result = await apiClient.setAIConfig({
        provider: 'openai',
        ...values,
      });
      if (result.success) {
        const testResult = await apiClient.testAIConnection();
        if (testResult.success) {
          message.success(testResult.message);
        } else {
          message.warning(testResult.message);
        }
      }
    } catch (error) {
      message.error('测试连接失败');
    } finally {
      setTestingConnection(false);
    }
  };

  const openSettings = async () => {
    await loadAIConfig();
    if (aiConfig) {
      form.setFieldsValue({
        provider: aiConfig.provider,
        model: aiConfig.model,
        base_url: aiConfig.base_url,
        temperature: aiConfig.temperature,
      });
    }
    setSettingsVisible(true);
  };

  return (
    <div className={styles.container}>
      <Card 
        title={
          <Space>
            <RobotOutlined />
            <span>AI 农场助手</span>
            {aiConfig && (
              <Tag 
                color={aiConfig.has_api_key ? 'green' : 'default'}
                icon={aiConfig.has_api_key ? <CheckCircleOutlined /> : <CloseCircleOutlined />}
              >
                {aiConfig.has_api_key ? '已配置' : '内置模式'}
              </Tag>
            )}
          </Space>
        }
        extra={
          <Button 
            icon={<SettingOutlined />} 
            onClick={openSettings}
          >
            API设置
          </Button>
        }
        className={styles.chatCard}
      >
        <div className={styles.messages}>
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`${styles.message} ${msg.role === 'user' ? styles.userMessage : styles.aiMessage}`}
            >
              <div className={styles.avatar}>
                {msg.role === 'user' ? <UserOutlined /> : <RobotOutlined />}
              </div>
              <div className={styles.content}>
                <div className={styles.bubble}>{msg.content}</div>
                {msg.suggestions && msg.suggestions.length > 0 && (
                  <div className={styles.suggestions}>
                    <Text type="secondary" className={styles.suggestionLabel}>试试这样问：</Text>
                    <Space wrap>
                      {msg.suggestions.map((s, i) => (
                        <Button
                          key={i}
                          size="small"
                          onClick={() => handleSuggestionClick(s)}
                          className={styles.suggestionButton}
                        >
                          {s}
                        </Button>
                      ))}
                    </Space>
                  </div>
                )}
              </div>
            </div>
          ))}
          {loading && (
            <div className={`${styles.message} ${styles.aiMessage}`}>
              <div className={styles.avatar}>
                <RobotOutlined />
              </div>
              <div className={styles.content}>
                <div className={styles.bubble}>
                  <Spin size="small" /> 思考中...
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        <div className={styles.inputArea}>
          <Input
            placeholder="输入你的问题..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onPressEnter={handleSend}
            disabled={loading}
            className={styles.input}
          />
          <Button
            type="primary"
            icon={<SendOutlined />}
            onClick={handleSend}
            loading={loading}
            className={styles.sendButton}
          >
            发送
          </Button>
        </div>
      </Card>

      <Modal
        title={
          <Space>
            <ApiOutlined />
            <span>AI API 配置</span>
          </Space>
        }
        open={settingsVisible}
        onCancel={() => setSettingsVisible(false)}
        footer={null}
        width={500}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSaveConfig}
        >
          <Form.Item
            label="AI 提供商"
            name="provider"
            initialValue="openai"
          >
            <Select>
              <Select.Option value="openai">OpenAI</Select.Option>
              <Select.Option value="anthropic">Anthropic (Claude)</Select.Option>
              <Select.Option value="custom">自定义 API</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="API 密钥"
            name="api_key"
            extra="留空则使用内置AI助手"
          >
            <Input.Password placeholder="输入你的API密钥" />
          </Form.Item>

          <Form.Item
            label="模型"
            name="model"
            initialValue="gpt-3.5-turbo"
          >
            <Select>
              <Select.Option value="gpt-3.5-turbo">GPT-3.5 Turbo</Select.Option>
              <Select.Option value="gpt-4">GPT-4</Select.Option>
              <Select.Option value="gpt-4-turbo">GPT-4 Turbo</Select.Option>
              <Select.Option value="claude-3-opus">Claude 3 Opus</Select.Option>
              <Select.Option value="claude-3-sonnet">Claude 3 Sonnet</Select.Option>
            </Select>
          </Form.Item>

          <Form.Item
            label="API 地址"
            name="base_url"
            initialValue="https://api.openai.com/v1"
          >
            <Input placeholder="自定义API地址" />
          </Form.Item>

          <Form.Item
            label="Temperature (创造性)"
            name="temperature"
            initialValue={0.7}
          >
            <InputNumber min={0} max={2} step={0.1} style={{ width: '100%' }} />
          </Form.Item>

          <Space>
            <Button 
              onClick={handleTestConnection}
              loading={testingConnection}
              disabled={!form.getFieldValue('api_key')}
            >
              测试连接
            </Button>
            <Button type="primary" htmlType="submit" loading={configLoading}>
              保存配置
            </Button>
          </Space>
        </Form>
      </Modal>
    </div>
  );
};

export default AIAssistant;
