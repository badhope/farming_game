import React, { useState, useEffect } from 'react';
import { 
  Card, Button, Typography, Breadcrumb, Space, 
  Progress, message, Tooltip, Divider, Tag, Row, Col 
} from 'antd';
import { 
  DownloadOutlined, FilePdfOutlined, FileZipOutlined, 
  GithubOutlined, HomeOutlined, LinkOutlined, 
  CheckCircleOutlined, CloudDownloadOutlined, 
  QuestionCircleOutlined, StarOutlined
} from '@ant-design/icons';
import { Link } from 'react-router-dom';
import styles from './Download.module.css';

const { Title, Paragraph, Text } = Typography;

interface DownloadFile {
  id: string;
  name: string;
  description: string;
  version: string;
  size: string;
  type: 'pdf' | 'zip' | 'exe';
  downloadCount: number;
  features: string[];
}

const downloadFiles: DownloadFile[] = [
  {
    id: 'game-v1.0',
    name: '农场大亨游戏完整版',
    description: '包含完整游戏内容、关卡、道具和多人模式',
    version: 'v1.0.0',
    size: '256 MB',
    type: 'zip',
    downloadCount: 12847,
    features: [
      '完整的游戏剧情模式',
      '5种难度级别',
      '50+种作物和道具',
      '成就系统',
      '统计面板'
    ]
  },
  {
    id: 'game-demo',
    name: '农场大亨试玩版',
    description: '体验版包含基础游戏内容',
    version: 'v1.0.0',
    size: '128 MB',
    type: 'zip',
    downloadCount: 5623,
    features: [
      '基础农场经营玩法',
      '3种难度选择',
      '20+种作物',
      '新手教程'
    ]
  },
  {
    id: 'guide-pdf',
    name: '游戏攻略指南',
    description: '详细的游戏玩法攻略和技巧',
    version: '2024.1',
    size: '15 MB',
    type: 'pdf',
    downloadCount: 8921,
    features: [
      '新手入门指南',
      '作物种植攻略',
      '商店购物技巧',
      '成就解锁指南',
      '常见问题解答'
    ]
  }
];

const Download: React.FC = () => {
  const [downloading, setDownloading] = useState<string | null>(null);
  const [downloadProgress, setDownloadProgress] = useState(0);
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsVisible(window.scrollY > 500);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleDownload = (file: DownloadFile, newWindow: boolean = false) => {
    setDownloading(file.id);
    setDownloadProgress(0);
    
    const interval = setInterval(() => {
      setDownloadProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval);
          setDownloading(null);
          message.success({
            content: `${file.name} 下载完成！`,
            duration: 3,
            icon: <CheckCircleOutlined style={{ color: '#52c41a' }} />
          });
          return 100;
        }
        return prev + Math.random() * 15;
      });
    }, 200);

    if (newWindow) {
      message.info('将在新窗口打开下载链接...');
    }
  };

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const getFileIcon = (type: string) => {
    switch (type) {
      case 'pdf':
        return <FilePdfOutlined style={{ fontSize: 48, color: '#ff4d4f' }} />;
      case 'zip':
        return <FileZipOutlined style={{ fontSize: 48, color: '#1890ff' }} />;
      default:
        return <DownloadOutlined style={{ fontSize: 48, color: '#52c41a' }} />;
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'pdf':
        return 'red';
      case 'zip':
        return 'blue';
      default:
        return 'green';
    }
  };

  return (
    <div className={styles.downloadPage}>
      <nav className={styles.navbar}>
        <div className={styles.navContent}>
          <Link to="/" className={styles.logo}>
            <span className={styles.logoIcon}>🌾</span>
            <span className={styles.logoText}>农场大亨</span>
          </Link>
          <div className={styles.navLinks}>
            <Link to="/">
              <Button type="text" icon={<HomeOutlined />}>
                首页
              </Button>
            </Link>
            <Button type="text" icon={<DownloadOutlined />} className={styles.activeNav}>
              下载中心
            </Button>
            <a href="https://github.com/badhope/farming_game" target="_blank" rel="noopener noreferrer">
              <Button type="text" icon={<GithubOutlined />}>
                GitHub
              </Button>
            </a>
          </div>
        </div>
      </nav>

      <main className={styles.main}>
        <div className={styles.header}>
          <div className={styles.container}>
            <Breadcrumb
              className={styles.breadcrumb}
              items={[
                { title: <Link to="/">首页</Link> },
                { title: '下载中心' }
              ]}
            />
            <Title level={1} className={styles.title}>
              <CloudDownloadOutlined className={styles.titleIcon} />
              下载中心
            </Title>
            <Paragraph className={styles.subtitle}>
              获取游戏客户端、攻略指南及最新版本更新
            </Paragraph>
            <div className={styles.stats}>
              <div className={styles.statItem}>
                <Text className={styles.statNumber}>27,391</Text>
                <Text className={styles.statLabel}>总下载量</Text>
              </div>
              <div className={styles.statDivider} />
              <div className={styles.statItem}>
                <Text className={styles.statNumber}>3</Text>
                <Text className={styles.statLabel}>可用资源</Text>
              </div>
              <div className={styles.statDivider} />
              <div className={styles.statItem}>
                <Text className={styles.statNumber}>2024</Text>
                <Text className={styles.statLabel}>最新更新</Text>
              </div>
            </div>
          </div>
        </div>

        <div className={styles.container}>
          <section className={styles.content}>
            <Title level={2} className={styles.sectionTitle}>
              推荐下载
            </Title>
            <Row gutter={[24, 24]}>
              {downloadFiles.map((file) => (
                <Col xs={24} lg={8} key={file.id}>
                  <Card
                    className={styles.downloadCard}
                    hoverable
                    actions={[
                      <Button
                        type="primary"
                        size="large"
                        icon={<DownloadOutlined />}
                        loading={downloading === file.id}
                        onClick={() => handleDownload(file, false)}
                        block
                      >
                        {downloading === file.id ? '下载中...' : '立即下载'}
                      </Button>,
                      <Button
                        size="large"
                        icon={<LinkOutlined />}
                        onClick={() => handleDownload(file, true)}
                        block
                      >
                        新窗口打开
                      </Button>
                    ]}
                  >
                    {downloading === file.id && (
                      <Progress 
                        percent={Math.min(Math.round(downloadProgress), 100)} 
                        status="active"
                        className={styles.downloadProgress}
                      />
                    )}
                    
                    <div className={styles.cardHeader}>
                      <div className={styles.fileIcon}>
                        {getFileIcon(file.type)}
                      </div>
                      <div className={styles.fileInfo}>
                        <Title level={4} className={styles.fileName}>
                          {file.name}
                        </Title>
                        <Space>
                          <Tag color={getTypeColor(file.type)}>
                            {file.type.toUpperCase()}
                          </Tag>
                          <Tag color="default">{file.version}</Tag>
                          <Tag color="default">{file.size}</Tag>
                        </Space>
                      </div>
                    </div>
                    
                    <Paragraph className={styles.fileDescription}>
                      {file.description}
                    </Paragraph>
                    
                    <Divider className={styles.featureDivider}>功能特点</Divider>
                    
                    <ul className={styles.featureList}>
                      {file.features.map((feature, index) => (
                        <li key={index}>
                          <CheckCircleOutlined className={styles.checkIcon} />
                          {feature}
                        </li>
                      ))}
                    </ul>
                    
                    <div className={styles.cardFooter}>
                      <Tooltip title="下载次数">
                        <span className={styles.downloadCount}>
                          <DownloadOutlined /> {file.downloadCount.toLocaleString()} 次下载
                        </span>
                      </Tooltip>
                    </div>
                  </Card>
                </Col>
              ))}
            </Row>
          </section>

          <section className={styles.notice}>
            <Card className={styles.noticeCard}>
              <Title level={4}>
                <QuestionCircleOutlined /> 下载须知
              </Title>
              <ul className={styles.noticeList}>
                <li>请确保网络连接稳定，建议使用WiFi下载</li>
                <li>下载完成后请检查文件完整性</li>
                <li>如遇下载问题，请尝试更换下载方式或联系技术支持</li>
                <li>本软件为开源项目，欢迎Star和Fork</li>
              </ul>
            </Card>
          </section>

          <section className={styles.qrSection}>
            <Card className={styles.qrCard}>
              <Row gutter={[48, 24]} align="middle">
                <Col xs={24} md={12}>
                  <div className={styles.qrContent}>
                    <Title level={3}>扫码关注我们</Title>
                    <Paragraph>
                      获取最新版本更新和游戏资讯
                    </Paragraph>
                    <Space size="large">
                      <div className={styles.qrPlaceholder}>
                        <span>二维码占位</span>
                      </div>
                      <div className={styles.socialLinks}>
                        <a href="https://github.com/badhope/farming_game" target="_blank" rel="noopener noreferrer">
                          <Button icon={<GithubOutlined />} size="large">
                            GitHub
                          </Button>
                        </a>
                        <Button icon={<StarOutlined />} size="large">
                          Star us
                        </Button>
                      </div>
                    </Space>
                  </div>
                </Col>
                <Col xs={24} md={12}>
                  <div className={styles.versionHistory}>
                    <Title level={4}>版本更新日志</Title>
                    <div className={styles.versionItem}>
                      <Tag color="green">最新</Tag>
                      <span>v1.0.0</span>
                      <Text type="secondary"> - 2024年1月</Text>
                    </div>
                    <div className={styles.versionItem}>
                      <span>v0.9.0</span>
                      <Text type="secondary"> - 2023年12月</Text>
                    </div>
                    <div className={styles.versionItem}>
                      <span>v0.8.5</span>
                      <Text type="secondary"> - 2023年11月</Text>
                    </div>
                  </div>
                </Col>
              </Row>
            </Card>
          </section>
        </div>
      </main>

      <footer className={styles.footer}>
        <div className={styles.container}>
          <Row gutter={[24, 24]}>
            <Col xs={24} md={8}>
              <div className={styles.footerSection}>
                <Title level={5}>关于项目</Title>
                <Paragraph className={styles.footerText}>
                  农场大亨是一款基于Web的模拟经营游戏，采用React + FastAPI技术栈开发。
                </Paragraph>
              </div>
            </Col>
            <Col xs={24} md={8}>
              <div className={styles.footerSection}>
                <Title level={5}>相关链接</Title>
                <div className={styles.footerLinks}>
                  <a href="https://github.com/badhope/farming_game" target="_blank" rel="noopener noreferrer">
                    <GithubOutlined /> GitHub仓库
                  </a>
                  <Link to="/">
                    <HomeOutlined /> 项目首页
                  </Link>
                  <a href="#">
                    <LinkOutlined /> 文档中心
                  </a>
                </div>
              </div>
            </Col>
            <Col xs={24} md={8}>
              <div className={styles.footerSection}>
                <Title level={5}>联系我们</Title>
                <Paragraph className={styles.footerText}>
                  技术支持：support@farmgame.com<br />
                  商务合作：biz@farmgame.com
                </Paragraph>
              </div>
            </Col>
          </Row>
          <Divider className={styles.footerDivider} />
          <div className={styles.copyright}>
            <Text type="secondary">
              © 2024 农场大亨项目团队. 基于MIT许可证开源.
            </Text>
          </div>
        </div>
      </footer>

      {isVisible && (
        <Button
          type="primary"
          shape="circle"
          size="large"
          icon={<LinkOutlined />}
          className={styles.backToTop}
          onClick={scrollToTop}
          aria-label="返回顶部"
        />
      )}
    </div>
  );
};

export default Download;
